
CREATE TABLE IF NOT EXISTS Admins
(
  AdminId VARCHAR(10) NOT NULL,
  Name VARCHAR(255),
  Email VARCHAR(255),
  Dept VARCHAR(32),
  Role VARCHAR(10),
  PRIMARY KEY (AdminId)
);

CREATE INDEX Admin_IX on Admins(Name);
CREATE INDEX Admin_Dept_IX on Admins(Dept, Name);


CREATE TABLE IF NOT EXISTS Assignments 
(
  AssignmentId VARCHAR(10) NOT NULL,
  RequestId VARCHAR(10),
  AdminId VARCHAR(10),
  PRIMARY KEY (AssignmentId)
);

CREATE INDEX Assignment_R_IX on Assignments(RequestId, AdminId);
CREATE INDEX Assignment_A_IX on Assignments(AdminId, RequestId);

