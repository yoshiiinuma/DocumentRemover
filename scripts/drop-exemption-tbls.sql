
DROP INDEX Filter_IX on Filters;
DROP INDEX Tag_IX on Tags;
DROP INDEX Communication_IX on Communications;
DROP INDEX Note_IX on Notes;
DROP INDEX Document_IX on Documents;

DROP INDEX Traveler_IX on Travelers;

DROP INDEX Request_User_IX on Requests;
DROP INDEX Request_ReqDate_IX on Requests;
DROP INDEX Request_Status_IX on Requests;
DROP INDEX Request_AppId_IX on Requests;
DROP INDEX Request_ApprovalId_IX on Requests;

DROP TABLE IF EXISTS States;
DROP TABLE IF EXISTS Filters;
DROP TABLE IF EXISTS Tags;
DROP TABLE IF EXISTS Communications;
DROP TABLE IF EXISTS Notes;
DROP TABLE IF EXISTS Documents;
DROP TABLE IF EXISTS Travelers;
DROP TABLE IF EXISTS Requests;
DROP TABLE IF EXISTS Users;

