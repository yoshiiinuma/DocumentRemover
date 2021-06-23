
CREATE VIEW TravelerExemptions
AS SELECT 
  TravelerId as ID,
  t.RequestId,
  r.`Approval ID` AS ApprovalId,
  r.Status AS RequestStatus,
  r.`Request Date` AS ApplicationDate,
  r.`Approval Date` AS ApprovalDate,
  `Last Name` AS LastName,
  `Middle Name` AS MiddleName,
  `First Name` AS FirstName,
  `Origin Country` AS OriginCountry,
  `Origin State` AS OriginState,
  `Destination Island` AS DestinationIsland,
  t.`Arrival Date` AS ArrivalDate,
  `Arrival Flight Number` AS ArrivalFlightNumber,
  `Departure Date` AS DepartureDate,
  `Departure Flight Number` AS DepartureFlightNumber,
  `Quarantine Location Type` AS QuarantineLocation,
  `Quarantine Location Address` AS QuarantineLocationAddress
FROM Travelers t
JOIN Requests r ON t.RequestId = r.RequestId
WHERE r.Status = 'Approved'
;

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


