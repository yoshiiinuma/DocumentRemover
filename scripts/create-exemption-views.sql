
CREATE VIEW RequestView
AS SELECT 
  RequestId,
  UserId,
  Owner,
  `Application Confirmation ID` AS ApplicationId,
  `Request Date` AS ApplicationDate,
  `Approval Date` AS ApprovalDate,
  IFNULL(TIME_TO_SEC(TIMEDIFF(`Approval Date`, `Request Date`)), 0) AS CompletedTime,
  Status,
  `Approval ID` AS ApprovalId,
  Assigned,
  AssignedHistory,
  `Travel Type` AS TravelType,
  `Exemption Category` AS ExemptionCategory,
  Purpose,
  `CISA Sub Category` AS CisaSubCategory,
  Details,
  `Project Document 1` AS ProofOfEmployment,
  `Project Document 1 Reviewed?` AS ProofOfEmploymentReviewed,
  `Project Document 2` AS AdditionalProofOfEmployment,
  `Project Document 2 Reviewed?` AS AdditionalProofOfEmploymentReviewed,
  `Proof of Port of Embarkation` AS PortOfEmbarkation,
  `Proof of Port of Embarkation Reviewed?` AS PortOfEmbarkationReviewed,
  `PCS Orders` AS PcsOrders,
  `PCS Orders Reviewed?` AS PcsOrdersReviewed,
  `Requestor` AS Requestor,
  `Requestor Name` AS RequestorName,
  `Requestor Email` AS RequestorEmail,
  CreatedAt,
  UpdatedAt,
  UpdatedBy
 FROM Requests;

CREATE VIEW TravelerView
AS SELECT 
  RequestId,
  TravelerId,
  Owner,
  `First Name` AS FirstName,
  `Middle Name` AS MiddleName,
  `Last Name` AS LastName,
  `Exemption Category` AS ExemptionCategory,
  `Origin Country` AS OriginCountry,
  `Origin State` AS OriginState,
  `Destination Island` AS DestinationIsland,
  `Arrival Date` AS ArrivalDate,
  `Arrival Flight Number` AS ArrivalFlightNumber,
  `Departure Date` AS DepartureDate,
  `Departure Flight Number` AS DepartureFlightNumber,
  IFNULL(DATEDIFF(`Departure Date`, `Arrival Date`), 0) AS Duration,
  Phone,
  `Quarantine Location Type` AS QuarantineLocation,
  `Quarantine Location Address` AS QuarantineLocationAddress,
  `Travel 14Days Before Arrival` AS Travel14DaysBeforeArrival,
  `Recent Travels` AS RecentTravels,
  `Picture ID` AS PictureId,
  CreatedAt,
  UpdatedAt,
  UpdatedBy
FROM Travelers;

CREATE VIEW ExemptionView
AS SELECT 
  t.RequestId,
  TravelerId,
  r.`Application Confirmation ID` AS ApplicationId,
  r.`Approval ID` AS ApprovalId,
  r.Status,
  r.`Exemption Category` AS ExemptionCategory,
  r.Purpose,
  r.`Request Date` AS ApplicationDate,
  r.`Approval Date` AS ApprovalDate,
  IFNULL(TIMEDIFF(r.`Approval Date`, r.`Request Date`), 0) AS CompletedTime,
  `Last Name` AS LastName,
  `First Name` AS FirstName,
  `Quarantine Location Type` AS QuarantineLocation,
  `Quarantine Location Address` AS QuarantineLocationAddress,
  `Destination Island` AS DestinationIsland,
  t.`Arrival Date` AS ArrivalDate,
  `Departure Date` AS DepartureDate,
  IFNULL(DATEDIFF(`Departure Date`, t.`Arrival Date`), 0) AS Duration,
  `Origin Country` AS OriginCountry,
  `Origin State` AS OriginState
FROM Travelers t
JOIN Requests r ON t.RequestId = r.RequestId;

