-- Use your database
USE COMP2001_HK_WLui;
GO

-- Create Location Table under CW2 schema
CREATE TABLE CW2.Location(
    LocationID INT PRIMARY KEY IDENTITY(1,1),
    Country VARCHAR(50) NOT NULL,
    City VARCHAR(50) NOT NULL,
    Area VARCHAR(50) NULL
);
GO

-- Create Trail Table under CW2 schema
CREATE TABLE CW2.Trail(
    TrailID INT PRIMARY KEY IDENTITY(1,1),
    TrailName VARCHAR(100) NOT NULL,
    Rating FLOAT CHECK (Rating >= 0 AND Rating <= 5),
    Difficulty VARCHAR(20) NOT NULL,
    Length FLOAT NOT NULL,
    ElevationGain INT NOT NULL,
    EstimatedTime VARCHAR(50) NOT NULL,
    Loop BIT NOT NULL,
    Description TEXT NULL,
    LocationID INT,
    FOREIGN KEY (LocationID) REFERENCES CW2.Location(LocationID)
);
GO

-- Create Sight Table under CW2 schema
CREATE TABLE CW2.Sight (
    SightID INT PRIMARY KEY IDENTITY(1,1),
    TrailID INT NOT NULL,
    SightName VARCHAR(100) NOT NULL,
    SightDescription TEXT NULL,
    SightLocation VARCHAR(100) NULL,
    FOREIGN KEY (TrailID) REFERENCES CW2.Trail(TrailID)
);
GO

-- Create TrailLog Table under CW2 schema
CREATE TABLE CW2.TrailLog (
    LogID INT PRIMARY KEY IDENTITY(1,1),
    TrailID INT,
    TrailName VARCHAR(100),
    user_name VARCHAR(50),
    ChangeDate DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (TrailID) REFERENCES CW2.Trail(TrailID)
);
GO