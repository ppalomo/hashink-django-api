# Hashink API

## Current endpoints

**Test:** https://hashink-api-test.herokuapp.com/

## Available methods

### Signer methods

Method | Entity | URL | Remarks | Parameters
------ | ------ | --- | ------- | ----------
GET | signer | /api/signer/ | Retrieve active signers list | -
GET | signer | /api/signer/[signer_id]/ | Retrieve signer detail | -
GET | signer | /api/signer/all/ | Retrieve signer and groups mixed list | -
GET | signer | /api/category/[category_id]/signers/ | Retrieve signers by category | -

### Groupsig methods

Method | Entity | URL | Remarks | Parameters
------ | ------ | --- | ------- | ----------
GET | groupsig | /api/groupsig/ | Retrieve active groups of signers list | -
GET | groupsig | /api/groupsig/[groupsig_id]/ | Retrieve groupsig detail | -

### Request methods

Method | Entity | URL | Remarks | Parameters
------ | ------ | --- | ------- | ----------
GET | request | /api/request/ | Retrieve requests list | -
GET | request | /api/request/[request_id]/ | Retrieve request detail | -
GET | request | /api/request/?requester_address__iexact=[requester_address] | Retrieve requests list by requester address | -
POST | request | /api/request/ | Create a new request for a single signer | requester_address, signer_id
POST | request | /api/request/ | Create a new request for a group of signers (groupsig) | requester_address, groupsig_id
DELETE | request | /api/request/[request_id] | Delete a request | -

### Category methods

Method | Entity | URL | Remarks | Parameters
------ | ------ | --- | ------- | ----------
GET | category | /api/category/ | Retrieve categories flat list | -
GET | category | /api/category/tree/ | Retrieve categories tree list | -
POST | category | /api/category/add_to_signer/[category_id]/[signer_id]/ | Add category to signer | -
DELETE | category | /api/category/delete_from_signer/[category_id]/[signer_id]/ | Remove category from signer | -

### Autograph methods

Method | Entity | URL | Remarks | Parameters
------ | ------ | --- | ------- | ----------
GET | autograph | /api/autograph/owner/[requester_address]/ | Retrieve autographs by requester | -
GET | autograph | /api/autograph/signer/[signer_address]/ | Retrieve autographs by signer | -