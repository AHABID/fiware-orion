/*
*
* Copyright 2017 Telefonica Investigacion y Desarrollo, S.A.U
*
* This file is part of Orion Context Broker.
*
* Orion Context Broker is free software: you can redistribute it and/or
* modify it under the terms of the GNU Affero General Public License as
* published by the Free Software Foundation, either version 3 of the
* License, or (at your option) any later version.
*
* Orion Context Broker is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero
* General Public License for more details.
*
* You should have received a copy of the GNU Affero General Public License
* along with Orion Context Broker. If not, see http://www.gnu.org/licenses/.
*
* For those usages not covered by this license please contact with
* iot_support at tid dot es
*
* Author: Ken Zangelin
*/
#include <string>
#include <vector>

#include "mongo/client/dbclient.h"

#include "logMsg/logMsg.h"
#include "logMsg/traceLevels.h"

#include "common/sem.h"
#include "common/statistics.h"
#include "common/errorMessages.h"
#include "rest/OrionError.h"
#include "rest/HttpStatusCode.h"
#include "apiTypesV2/Registration.h"
#include "mongoBackend/dbConstants.h"
#include "mongoBackend/safeMongo.h"
#include "mongoBackend/MongoGlobal.h"
#include "mongoBackend/connectionOperations.h"
#include "mongoBackend/MongoCommonRegister.h"
#include "mongoBackend/mongoRegistrationGet.h"



/* ****************************************************************************
*
* mongoRegistrationGet - 
*/
void mongoRegistrationGet
(
  ngsiv2::Registration*  regP,
  const std::string&     regId,
  const std::string&     tenant,
  const std::string&     servicePath,
  OrionError*            oeP
)
{
  bool         reqSemTaken = false;
  std::string  err;
  mongo::OID   oid;
  StatusCode   sc;

  if (safeGetRegId(regId, &oid, &sc) == false)
  {
    oeP->fill(sc);
    return;
  }

  reqSemTake(__FUNCTION__, "Mongo Get Registration", SemReadOp, &reqSemTaken);

  LM_T(LmtMongo, ("Mongo Get Registration"));

  std::auto_ptr<mongo::DBClientCursor>  cursor;
  mongo::BSONObj                        q;

  // FIXME P0: what about the service path ... ?   See issue #3051
  q = BSON("_id" << oid);

  TIME_STAT_MONGO_READ_WAIT_START();
  mongo::DBClientBase* connection = getMongoConnection();
  if (!collectionQuery(connection, getRegistrationsCollectionName(tenant), q, &cursor, &err))
  {
    releaseMongoConnection(connection);
    TIME_STAT_MONGO_READ_WAIT_STOP();
    reqSemGive(__FUNCTION__, "Mongo Get Registration", reqSemTaken);
    oeP->fill(SccReceiverInternalError, err);
    return;
  }
  TIME_STAT_MONGO_READ_WAIT_STOP();

  /* Process query result */
  if (moreSafe(cursor))
  {
    mongo::BSONObj r;
    if (!nextSafeOrErrorF(cursor, &r, &err))
    {
      releaseMongoConnection(connection);
      LM_E(("Runtime Error (exception in nextSafe(): %s - query: %s)", err.c_str(), q.toString().c_str()));
      reqSemGive(__FUNCTION__, "Mongo Get Registration", reqSemTaken);
      oeP->fill(SccReceiverInternalError, std::string("exception in nextSafe(): ") + err.c_str());
      return;
    }
    LM_T(LmtMongo, ("retrieved document: '%s'", r.toString().c_str()));

    //
    // Fill in the Registration with data retrieved from the data base
    //
    mongoRegistrationIdExtract(regP, r);
    mongoDescriptionExtract(regP, r, REG_DESCRIPTION);

    if (mongoDataProvidedExtract(regP, r, false, REG_CONTEXT_REGISTRATION) == false)
    {
      releaseMongoConnection(connection);
      LM_W(("Bad Input (getting registrations with more than one CR is not yet implemented, see issue 3044)"));
      reqSemGive(__FUNCTION__, "Mongo Get Registration", reqSemTaken);
      oeP->fill(SccReceiverInternalError, err);
      return;
    }

    mongoExpiresExtract(regP, r, REG_EXPIRATION);
    mongoStatusExtract(regP, r, REG_STATUS);
    mongoForwardingInformationExtract(regP, r, REG_FORWARDING_INFORMATION);
    
    if (moreSafe(cursor))  // Can only be one ...
    {
      releaseMongoConnection(connection);
      LM_T(LmtMongo, ("more than one registration: '%s'", regId.c_str()));
      reqSemGive(__FUNCTION__, "Mongo Get Registration", reqSemTaken);
      oeP->fill(SccConflict, "");
      return;
    }
  }
  else
  {
    releaseMongoConnection(connection);
    LM_T(LmtMongo, ("registration not found: '%s'", regId.c_str()));
    reqSemGive(__FUNCTION__, "Mongo Get Registration", reqSemTaken);
    oeP->fill(SccContextElementNotFound, ERROR_DESC_NOT_FOUND_REGISTRATION, ERROR_NOT_FOUND);

    return;
  }

  releaseMongoConnection(connection);
  reqSemGive(__FUNCTION__, "Mongo Get Registration", reqSemTaken);

  oeP->fill(SccOk, "");
}
