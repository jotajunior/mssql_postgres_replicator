ALTER DATABASE beblue_prod  
SET CHANGE_TRACKING = ON  
(CHANGE_RETENTION = 5 DAYS, AUTO_CLEANUP = ON);

ALTER TABLE dbo.CashBackAccount   
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.CashBackAccount TO beblue_portal;

ALTER TABLE dbo.CashBackAccountTransaction   
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.CashBackAccountTransaction TO beblue_portal;

ALTER TABLE dbo.CashBackAccountTransactionData    
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.CashBackAccountTransactionData TO beblue_portal;

ALTER TABLE dbo.CashBackAccountTransactionMerchant 
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.CashBackAccountTransactionMerchant TO beblue_portal;

ALTER TABLE dbo.CashBackAccountTransactionParcel 
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.CashBackAccountTransactionParcel TO beblue_portal;

ALTER TABLE dbo.CashBackAccountTransferer 
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.CashBackAccountTransferer TO beblue_portal;

ALTER TABLE dbo.CashBackDailyTransactionByCustomer  
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.CashBackDailyTransactionByCustomer TO beblue_portal;

ALTER TABLE dbo.CashBackInviteFriends 
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.CashBackInviteFriends TO beblue_portal;

ALTER TABLE dbo.CashBackInvites   
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.CashBackInvites TO beblue_portal;

ALTER TABLE dbo.CashBackTransactionType  
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.CashBackTransactionType TO beblue_portal;

ALTER TABLE dbo.CashbackInviteRedeem    
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.CashbackInviteRedeem TO beblue_portal;

ALTER TABLE dbo.ClientMerchants 
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.ClientMerchants TO beblue_portal;

ALTER TABLE dbo.ClientMerchantsCashBack 
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.ClientMerchantsCashBack TO beblue_portal;

ALTER TABLE dbo.ClientMerchantsTransactions  
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.ClientMerchantsTransactions TO beblue_portal;

ALTER TABLE dbo.Customers    
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.Customers TO beblue_portal;

ALTER TABLE dbo.EstablishmenTypes   
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.EstablishmenTypes TO beblue_portal;

ALTER TABLE dbo.MarketPlaceAccount    
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.MarketPlaceAccount TO beblue_portal;

ALTER TABLE dbo.MarketPlaceAccountTransaction   
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.MarketPlaceAccountTransaction TO beblue_portal;

ALTER TABLE dbo.MerchantCoverImages  
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.MerchantCoverImages TO beblue_portal;

ALTER TABLE dbo.Merchants 
ENABLE CHANGE_TRACKING   
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.Merchants TO beblue_portal;

ALTER TABLE dbo.MerchantsRatings   
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.MerchantsRatings TO beblue_portal;

ALTER TABLE dbo.CashbackAccountTransactionRating 
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.CashbackAccountTransactionRating TO beblue_portal;

ALTER TABLE dbo.CashbackAccountTransactionRatingTags   
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.CashbackAccountTransactionRatingTags TO beblue_portal;

ALTER TABLE dbo.CashbackVoucher    
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.CashbackVoucher TO beblue_portal;

ALTER TABLE dbo.CashbackVoucherCustomer    
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.CashbackVoucherCustomer TO beblue_portal;

ALTER TABLE dbo.CashbackSurvey  
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.CashbackSurvey TO beblue_portal;

ALTER TABLE dbo.CashbackQuestion
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.CashbackQuestion TO beblue_portal;

ALTER TABLE dbo.CashbackSurveyQuestion
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.CashbackSurveyQuestion TO beblue_portal;

ALTER TABLE dbo.CashbackSurveySent
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.CashbackSurveySent TO beblue_portal;

ALTER TABLE dbo.CashbackAnswer
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.CashbackAnswer TO beblue_portal;

ALTER TABLE dbo.MarketplaceBulkAnticipationsTransactions
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.MarketplaceBulkAnticipationsTransactions TO beblue_portal;

ALTER TABLE dbo.Sale
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.Sale TO beblue_portal;

ALTER TABLE dbo.SaleInstallment
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.SaleInstallment TO beblue_portal;

ALTER TABLE dbo.SaleStatus
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.SaleStatus TO beblue_portal;

ALTER TABLE dbo.SaleType
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.SaleType TO beblue_portal;

ALTER TABLE dbo.MerchantBalanceOperation
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.MerchantBalanceOperation TO beblue_portal;

ALTER TABLE dbo.MovementType
ENABLE CHANGE_TRACKING  
WITH (TRACK_COLUMNS_UPDATED = ON);
GRANT VIEW CHANGE TRACKING ON OBJECT::dbo.MovementType TO beblue_portal;

ALTER DATABASE beblue_prod  
    SET ALLOW_SNAPSHOT_ISOLATION ON;  
