
CREATE VIEW CISATravelerExemptions
AS SELECT 
  m.MemberId as ID,
  m.`Approval ID` AS ApprovalId,
  o.Status AS AgreementStatus,
  o.OrganizationId,
  o.`Organization Name` AS OrganizationName,
  m.Status AS TravelerStatus,
  m.`Last Name` AS LastName,
  m.`Middle Name` AS MiddleName,
  m.`First Name` AS FirstName
FROM Members m
JOIN Organizations o ON o.OrganizationId = m.OrganizationId
WHERE m.Status = 'Active'
  AND o.Status = 'Approved'
;
