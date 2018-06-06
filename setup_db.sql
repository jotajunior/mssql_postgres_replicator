CREATE INDEX ON marketplaceaccounttransaction (transactioncode);
CREATE INDEX ON cashbackaccounttransaction (operationcode);
CREATE INDEX ON marketplaceaccounttransaction (clientmerchantid);
CREATE INDEX ON marketplaceaccounttransaction (CAST(transactiondate AS DATE));
