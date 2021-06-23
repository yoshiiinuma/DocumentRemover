
CREATE TABLE IF NOT EXISTS Assignees
(
  Team VARCHAR(64),
  Name VARCHAR(255),
  Email VARCHAR(255),
  PRIMARY KEY (Name)
);

CREATE INDEX Assignees_TeamName_IX on Assignees(Team, Name);

Insert Into Assignees (Team, Name) Values
('AG','Admin: Lori Tanigawa'),('AG','Admin: Stella Kam'),('AG','CED: Andrew Goff'),('AG','CED: Daniel Jacob'),('AG','CED: James Paige'),('AG','CED: Jodi Yi'),('AG','CED: Kelly Suzuka'),('AG','CED: Lori Sunakoda'),('AG','CJD: David Williams'),('AG','CJD: Delanie Prescott-Tate'),('AG','CJD: Farshad Talebi'),('AG','CJD: Richard Stacey'),('AG','CRD: Kotoba Kanazawa'),('AG','CRD: Ruth Oh'),('AG','CSEA: Brandon Flores'),('Recovered','DCCA: Arlene Ige'),('Recovered','DCCA: Ahlani Quiogue'),('Recovered','DCCA: Bruce Schoenberg'),('Recovered','DCCA: Catherine Awakuni Colón'),('Recovered','DCCA: Craig Uyehara'),('Recovered','DCCA: Desiree Hikida'),('Recovered','DCCA: Denise Balanay'),('Recovered','DCCA: Dwight Young'),('Recovered','DCCA: Glenn Taka'),('Recovered','DCCA: Gordan Ito'),('Recovered','DCCA: Henry Tanji'),('Recovered','DCCA: Iris Ikeda'),('Recovered','DCCA: James Chee'),('Recovered','DCCA: Jamie Sheu'),('Recovered','DCCA: Jayson Horiuchi'),('Recovered','DCCA: Jayson Kauwenaole'),('Recovered','DCCA: Ji Sook Kim'),('Recovered','DCCA: Jo Ann Uchida Takeuchi'),('Recovered','DCCA: Karyn Takahashi'),('Recovered','DCCA: Kyle Kagihara'),('Recovered','DCCA: Marc Hirai'),('Recovered','DCCA: Robert Hiltner'),('Recovered','DCCA: Rodney Ching'),('Recovered','DCCA: Tara L. Murphy'),('AG','DOH: Keisha Willis'),('AG','DOT: Michele Latimer'),('AG','DOT: Curtis Motoyama'),('AG','DOT: David Rodriguez'),('AG','DOT: Derek Chow'),('AG','DOT: Jazelle Aolahiko'),('AG','DOT: Juli Chun'),('AG','DOT: Karen Awana'),('AG','DOT: Lynn Araki-Regan'),('AG','DOT: Melanie Martin'),('AG','DOT: Pradip Pant'),('AG','DOT: Ryan Aguilar'),('AG','DOT: Shelly Kunishige'),('AG','DOT: Zachariah Wadsack'),('AG','EDU: Anne Horiuchi'),('AG','EDU: Kevin Richardson'),('AG','EDU: Kris Murakami'),('AG','EDU: Melissa Kolonie'),('AG','ELD: Amanda Furman'),('AG','ELD: Grant Giventer'),('AG','ELD: Quinn Yang'),('AG','FLD: Eric Alabanza'),('AG','FLD: Ian Tsuda'),('AG','FLD: Jonathan Fujiyama'),('AG','FLD: Kellie Kersten'),('AG','FLD: Lianne Onishi'),('AG','FLD: Scott Boone'),('AG','GOV: Kymberly Sparlin'),('AG','HEALTH: Andrea Armitage'),('AG','HEALTH: Meegan Zane'),('AG','HEALTH: Scott Fujimoto'),('AG','HEALTH: Shaun Hirai'),('AG','HEALTH: Valerie Kato'),('AG','HEALTH: Wade Hargrove'),('AG','HSD: Erin Yamashiro'),('AG','HSD: Lili Young'),('AG','HSD: Lynne Youmans'),('AG','HSD: Melissa Lewis'),('AG','L/T: Duane Kokesch'),('AG','L/T: Goldman, Melissa D'),('AG','L/T: Julie China'),('AG','LTD: Marjie Lau'),('AG','LBR: Adam Rosenberg'),('AG','LBR: Staci Teruya'),('AG','OAG: Krishna Jayaram'),('AG','PSHH: Craig Iha'),('AG','PSHH: Daryl Akamichi'),('AG','PSHH: Donna Hoeft'),('AG','PSHH: Janet Salsedo'),('AG','PSHH: Jennifer Tran'),('AG','PSHH: John Henry'),('AG','PSHH: Klemen Urbanc'),('AG','PSHH: Laura Maeshiro'),('AG','PSHH: Lisa Itomura'),('AG','PSHH: Michelle Agsalda'),('AG','PSHH: Sandra Ching'),('AG','TAX: Kristen Sakamoto'),('AG','TAX: Kristie Chang'),('AG','TAX: Mary Yokota'),('AG','TAX: Patrick Kelly'),('Recovered','DCCA: Bobbi Lum-Mew'),('Recovered','DCCA: James Hogarty'),('Recovered','DCCA: Kathleen Dobrowolski'),('Recovered','DCCA: Marjorie Bragado'),('Recovered','DCCA: Xiaohong Kozel'),('Recovered','DCCA: Sharon Kunimoto'),('Recovered','DCCA: Homer Yung'),('Recovered','DCCA: Reyna Leong'),('Recovered','DCCA: Jayme Sakai'),('Recovered','DCCA: Adrienne Teshima'),('Recovered','DCCA: Yolanda Frazier'),('Recovered','DCCA: Lee Leonard'),('Recovered','DCCA: Layla Kilolu'),('Recovered','DCCA: Gena Yoshida'),('Recovered','DCCA: Jonathan Tumacder'),('Recovered','DCCA: Randy Cortez'),('Recovered','DCCA: Todd Okuda'),('Recovered','DCCA: Leysilie Williams'),('Recovered','DCCA: Courtney DeCenzo'),('Recovered','DCCA: Kyle Diego'),('Recovered','DCCA: Janice Lee'),('Recovered','DCCA: Karen Axsom'),('Recovered','DCCA: Elizabeth Pomeroy-Theoret'),('Recovered','DCCA: Mavis Okihara'),('Recovered','DCCA: Sheryl Robinol'),('Recovered','DCCA: Tiffany Zygarewicz'),('Recovered','DCCA: Chelsea Fukunaga'),('Recovered','DCCA: Lei Ana Green'),('Recovered','DCCA: Mona Caneso-Bantolina'),('Recovered','DCCA: Scot Robertson'),('Recovered','DCCA: Taylor Horninger'),('Recovered','DCCA: Sarah Tribble');

CREATE VIEW SortedAssignees
    AS SELECT Team, Name, Email
  FROM Assignees
 ORDER BY Team, Name;