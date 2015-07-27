/*
*
* Copyright 2015 Telefonica Investigacion y Desarrollo, S.A.U
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
* Author: Orion dev team
*/
#include <string>
#include <vector>

#include "rest/ConnectionInfo.h"
#include "ngsi/ParseData.h"
#include "apiTypesV2/Entities.h"
#include "rest/EntityTypeInfo.h"
#include "serviceRoutinesV2/postAttributes.h"
#include "serviceRoutines/postUpdateContext.h"




#include "logMsg/logMsg.h"
#include "logMsg/traceLevels.h"


/* ****************************************************************************
*
* postAttributes -
*
* POST /v2/entities/{entityId}
*
* Payload In:  Attributes
* Payload Out: None
*
* URI parameters:
*   -
*/
std::string postAttributes
(
  ConnectionInfo*            ciP,
  int                        components,
  std::vector<std::string>&  compV,
  ParseData*                 parseDataP
)
{
  Entity*  eP = &parseDataP->ent.res;
  eP->id = compV[2];


  std::string op = ciP->uriParam["op"];
   LM_W(("OP: '%s'", op.c_str()));
  if (op == "")
  {
   op = "APPEND";   // append or update

  }
  else if (op == "append") // pure-append
  {
   op = "UPDATE";
  }
  else
  {
    ciP->httpStatusCode = SccBadRequest;
    return "{\"ERROR\": \"What in hell is '"+op+"'?\"}";
  }
  // Fill in UpdateContextRequest
  parseDataP->upcr.res.fill(eP, op);

  // Call standard op postUpdateContext
  postUpdateContext(ciP, components, compV, parseDataP);


  // Prepare status code
  if (ciP->httpStatusCode == SccOk || ciP->httpStatusCode == SccNone) {
      ciP->httpStatusCode = SccNoContent;
  }

  // Cleanup and return result
  eP->release();

  return "";
}
