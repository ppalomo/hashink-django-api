# Hashink API

## Current endpoints

**Test:** https://hashink-api-test.herokuapp.com/

## Available methods

### Retrieve signers list
```
Method=GET
/api/signer/
```

### Retrieve signer detail
```
Method=GET
/api/signer/[signer_id]/
```

### Retrieve signer groups list
```
Method=GET
/api/groupsig/
```

### Retrieve group detail
```
Method=GET
/api/groupsig/[groupsig_id]/
```

### Retrieve signer and groups mixed list
```
Method=GET
/api/signer/all/
```

### Retrieve requests list
```
Method=GET
/api/request/
```

### Retrieve requester requests list (by requester address)
```
Method=GET
/api/request/?requester_address__iexact=[requester_address]
```

### Retrieve request detail
```
Method=GET
/api/request/[request_id]/
```

## Retrieve categories flat list
```
Method=GET
/api/category/
```

## Retrieve categories tree list
```
Method=GET
/api/category/tree/
```

## Retrieve signers by category
```
Method=GET
/api/category/[category_id]/signers/
```

## Retrieve autographs by requester
```
Method=GET
/api/autograph/owner/[requester_address]/
```

## Retrieve autographs by signer
```
Method=GET
/api/autograph/signer/[signer_address]/
```
