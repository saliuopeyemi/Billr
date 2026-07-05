# Billr Backend Documentation


## Index<a name='toc'></a>

{{TOC}}


# Merchant Register

This API allows registering of a merchant. N.B:A merchant admin is automatically created for the merchant.

**Endpoint:**`/merchant/register/`

**Method:** `POST`

## Payload

``` json
{

'business_email':'*****',

'business_name':'*****',

'business_type':'*****',

'phone_number':'*****',

'full_name':'*****',

'password1':'*****',

'password2':'*****',

'web_url (**optional)':'*****',

}

```
## Response body

**status code:201**

``` json
{
  "id": 7,
  "business_name": "Maytechstop",
  "business_email": "maytechstop@yopmail.com",
  "phone_number": "07032812713",
  "business_type": "saas",
  "web_url": null,
  "test_api_key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZXJjaGFudF9pZCI6NywibWVyY2hhbnRfbmFtZSI6Ik1heXRlY2hzdG9wIiwibWVyY2hhbnRfZW1haWwiOiJtYXl0ZWNoc3RvcEB5b3BtYWlsLmNvbSIsImVudHJvcHkiOjE3ODMyNDEwODMuNjMzMzEwMywia2V5X3R5cGUiOiJURVNUIn0.mlRyXwdQx8Fba9XyHFqUbnqsw-YuLbvssJqznsl_we0"
}
```

[["/merchant/register/","POST"]][Table of contents](#toc)


# Login

This API allows any user to Login into the system.

**Endpoint:**`user/signin/`

**Method:** `POST`

## Payload

``` json
{

"email":"*****",

"password":"*****",

}

```
## Response body

**status code:200**

``` json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MzMxMDUwOSwiaWF0IjoxNzgzMjI0MTA5LCJqdGkiOiJjZTE2OGQ0YjI2ZTk0OTNlOWY4YTVkYjcxY2ZiMzU3YyIsInVzZXJfaWQiOiIzIn0.iSv6VK0sb9ZJnfHA6qHT4oDagZLwEBNrov_YuqGTovY",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzgzMjQ1NzA5LCJpYXQiOjE3ODMyMjQxMDksImp0aSI6ImJiMTcyZGUyNzZiNjRjNzk4MTY0ZWU1NTM1M2E2YzZkIiwidXNlcl9pZCI6IjMifQ.2_XbH5Mdum8exynJyjlacJ7CGXdY4PhaO6RjGeQNKA4",
  "user": {
    "id": 3,
    "full_name": "Opeyemi Abdul Azeez",
    "email": "maytechstop@yopmail.com",
    "user_type": "merchant_admin",
    "related_merchant": {
      "id": 3,
      "business_name": "Maytechstop",
      "business_email": "maytechstop@yopmail.com",
      "phone_number": "07032812713",
      "business_type": "saas",
      "web_url": null
    }
  }
}
```

[["user/signin/","POST"]][Table of contents](#toc)


# Confirm Otp

This API confirms a Login OTP in the case where a user enables 2fa.

**Endpoint:**`/user/signin/confirm-otp/`

**Method:** `POST`

## Payload

``` json
{

"email":"*****",

"otp":"*****",

}

```
## Response body

**status code:200**

``` json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MzMxNDU3OSwiaWF0IjoxNzgzMjI4MTc5LCJqdGkiOiJkZDhiMWQ3NWI2Yjk0ZDRiOTc4ODg5MjdlN2U4OGU3NiIsInVzZXJfaWQiOiIzIn0.JQqWLDVE93u73cHHXpgNK_4Wac-bB0w2lUgHtd7gsNw",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzgzMjQ5Nzc5LCJpYXQiOjE3ODMyMjgxNzksImp0aSI6IjIwNmFlYzU4NTQ3YTQzYzRiZjdiZDBhZGNiYjg1NTFhIiwidXNlcl9pZCI6IjMifQ.HHIQovtTFsmGA2qXugWBM2uKJyGhEDlpCMlJQ6lJAvk",
  "user": {
    "id": 3,
    "full_name": "Opeyemi Abdul Azeez",
    "email": "maytechstop@yopmail.com",
    "user_type": "merchant_admin",
    "related_merchant": {
      "id": 3,
      "business_name": "Maytechstop",
      "business_email": "maytechstop@yopmail.com",
      "phone_number": "07032812713",
      "business_type": "saas",
      "web_url": null
    }
  }
}
```

[["/user/signin/confirm-otp/","POST"]][Table of contents](#toc)