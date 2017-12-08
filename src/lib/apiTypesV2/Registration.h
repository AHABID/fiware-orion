#ifndef SRC_LIB_APITYPESV2_REGISTRATION_H_
#define SRC_LIB_APITYPESV2_REGISTRATION_H_

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
* Author: Fermín Galán Márquez
*/
#include <string>
#include <vector>

#include "apiTypesV2/EntID.h"


#if 0
------------------------------------------------------------------------------------
  FIXME: Reference registration document (delete once POST /v2/registrations get implemented)

  {
    "id": "abcdefg",
    "description": "Example Context Source",
    "dataProvided": {
      "entities": [
        {
          "id": "Bcn_Welt",
          "type": "Room"
        }
      ],
      "attrs": [
        "temperature"
      ]
    },
    "provider": {
      "http": {
        "url": "http://contextsource.example.org"
      },
      "supportedForwardingMode": "all",
      "legacyForwarding": true
    },
    "expires": "2017-10-31T12:00:00",
    "status": "failed",
    "forwardingInformation": {
      "timesSent": 12,
      "lastForwarding": "2017-10-06T16:00:00.00Z",
      "lastFailure": "2017-10-06T16:00:00.00Z",
      "lastSuccess": "2017-10-05T18:25:00.00Z",
    }
  }
------------------------------------------------------------------------------------
#endif


namespace ngsiv2
{

/* ****************************************************************************
*
* ForwardingInformation -
*/
class ForwardingInformation
{
public:
  long long    lastFailure;
  long long    lastSuccess;
  long long    timesSent;
  long long    lastForwarding;

  ForwardingInformation();
  std::string  toJson();
};



/* ****************************************************************************
*
* Provider -
*/
struct Provider
{
  std::string  url;

  std::string  toJson();
};



/* ****************************************************************************
*
* DataProvided -
*/
struct DataProvided
{
  std::vector<EntID>        entities;
  std::vector<std::string>  attributes;

  std::string               toJson();
};



/* ****************************************************************************
*
* Registration -
*/
struct Registration
{
  std::string            id;
  std::string            servicePath;
  std::string            description;
  bool                   descriptionProvided;
  DataProvided           dataProvided;
  long long              expires;
  std::string            status;
  Provider               provider;
  ForwardingInformation  forwardingInformation;

  Registration();
  ~Registration();
  std::string            toJson();
};

}

#endif  // SRC_LIB_APITYPESV2_REGISTRATION_H_
