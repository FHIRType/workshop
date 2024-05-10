api_description = {
    "getdata": "Retrieve data from all endpoints or specified endpoints. Given a first name, last name, and NPI the routes retrieve data from all endpoints or specified endpoints. This will return data as JSON, a file, or web page based on their queries. Optionally it could contain an attribute to limit or specify the endpoints used to gather data.",
    "getlistdata": "Retrieve data from all endpoints or specified endpoints. Given a first name, last name, and NPI returns list of standard objects indexed by NPI number. This will return data as JSON, a file, or web page based on their queries. Replace npi to real value, and fill out the body. Format can be null. (options = page, file)",
    "getconsensus": "Given a group of matched records, return those records with a consensus result and an accuracy score built in.",
    "matchdata": "Given a list of JSON of flattened data, the service should attempt to match records and return all records as list of lists.",
    "askai": "The AI will group the provided data into separate lists based off of their NPI, and Street address. Will return the most accurate information to the user."
}
