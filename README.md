# Hashink API

## Current endpoints

**Test:** https://hashink-api-test.herokuapp.com/
**Prod:** https://hashink-api.herokuapp.com/

## Database schema

![alt text](https://github.com/ppalomo/hashink-django-api/blob/master/staticfiles/db_schema.jpeg?raw=true)

## Available methods

### Signer methods

| Method | Entity | URL                            | Remarks                                  | Parameters                                                                                       |
| ------ | ------ | ------------------------------ | ---------------------------------------- | ------------------------------------------------------------------------------------------------ |
| GET    | signer | /api/signer/                   | Retrieve active signers list             | -                                                                                                |
| GET    | signer | /api/signer/[signer_id]/       | Retrieve signer detail                   | -                                                                                                |
| GET    | signer | /api/signer/all/               | Retrieve signer and groups mixed list    | -                                                                                                |
| POST   | signer | /api/signer/                   | Create a new signer                      | first_name, last_name, email, address, price, response_time, avatar (binary), autograph (binary) |
| PATCH  | signer | /api/signer/[signer_id]        | Update a signer                          | Field to update                                                                                  |
| DELETE | signer | /api/signer/[signer_id]        | Delete a signer                          | -                                                                                                |
| POST   | signer | /api/signer/[signer_id]/print/ | Increments number of prints for a signer | -                                                                                                |

### Groupsig methods

| Method | Entity   | URL                          | Remarks                                | Parameters                                  |
| ------ | -------- | ---------------------------- | -------------------------------------- | ------------------------------------------- |
| GET    | groupsig | /api/groupsig/               | Retrieve active groups of signers list | -                                           |
| GET    | groupsig | /api/groupsig/[groupsig_id]/ | Retrieve groupsig detail               | -                                           |
| POST   | groupsig | /api/groupsig/               | Create a new groupsig                  | name, price, response_time, avatar (binary) |
| PATCH  | groupsig | /api/groupsig/[groupsig_id]  | Update a groupsig                      | Field to update                             |
| DELETE | groupsig | /api/groupsig/[groupsig_id]  | Delete a groupsig                      | -                                           |

### Request methods

| Method | Entity  | URL                                                           | Remarks                                                | Parameters                     |
| ------ | ------- | ------------------------------------------------------------- | ------------------------------------------------------ | ------------------------------ |
| GET    | request | /api/request/                                                 | Retrieve requests list                                 | -                              |
| GET    | request | /api/request/[request_id]/                                    | Retrieve request detail                                | -                              |
| GET    | request | /api/request/?requester_address\_\_iexact=[requester_address] | Retrieve requests list by requester address            | -                              |
| POST   | request | /api/request/                                                 | Create a new request for a single signer               | requester_address, signer_id   |
| POST   | request | /api/request/                                                 | Create a new request for a group of signers (groupsig) | requester_address, groupsig_id |
| POST   | request | /api/request/[request_id]/mint/                               | Mint an existing request                               | -                              |
| DELETE | request | /api/request/[request_id]                                     | Delete a request                                       | -                              |

### Category methods

| Method | Entity   | URL                                                         | Remarks                               | Parameters |
| ------ | -------- | ----------------------------------------------------------- | ------------------------------------- | ---------- |
| GET    | category | /api/category/                                              | Retrieve categories flat list         | -          |
| GET    | category | /api/category/tree/                                         | Retrieve categories tree list         | -          |
| GET    | category | /api/category/[category_id]/                                | Retrieve category detail with signers | -          |
| POST   | category | /api/category/add_to_signer/[category_id]/[signer_id]/      | Add category to signer                | -          |
| DELETE | category | /api/category/delete_from_signer/[category_id]/[signer_id]/ | Remove category from signer           | -          |

### Autograph methods

| Method | Entity    | URL                                       | Remarks                          | Parameters |
| ------ | --------- | ----------------------------------------- | -------------------------------- | ---------- |
| GET    | autograph | /api/autograph/owner/[requester_address]/ | Retrieve autographs by requester | -          |
| GET    | autograph | /api/autograph/signer/[signer_address]/   | Retrieve autographs by signer    | -          |

### Charity methods

| Method | Entity  | URL                        | Remarks                 | Parameters |
| ------ | ------- | -------------------------- | ----------------------- | ---------- |
| GET    | charity | /api/charity/              | Retrieve charities list | -          |
| GET    | charity | /api/charity/[charity_id]/ | Retrieve charity detail | -          |

### Drop methods

| Method | Entity | URL                          | Remarks                | Parameters                                 |
| ------ | ------ | ---------------------------- | ---------------------- | ------------------------------------------ |
| GET    | drop   | /api/drop/                   | Retrieve drops list    | -                                          |
| GET    | drop   | /api/drop/[drop_id]/         | Retrieve drop detail   | -                                          |
| POST   | drop   | /api/drop/[drop_id]/request/ | Creates a drop request | requester_address, message, image (binary) |
