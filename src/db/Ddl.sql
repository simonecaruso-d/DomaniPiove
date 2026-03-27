-- City
CREATE TABLE "City" (
    "Id" INT PRIMARY KEY,
    "City" VARCHAR(100) NOT NULL,
    "Latitude" NUMERIC(8,6) NOT NULL,
    "Longitude" NUMERIC(9,6) NOT NULL,
    "Province" VARCHAR(100) NOT NULL,
    "State" VARCHAR(100) NOT NULL,
    "Country" VARCHAR(100) NOT NULL,
    "Region" VARCHAR(100) NOT NULL,
    "CreatedAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "UpdatedAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP);

CREATE INDEX "IdxCityId" ON "City" ("Id");
CREATE INDEX "IdxCityCountry" ON "City" ("Country");

-- Calendar
CREATE TABLE "Calendar" (
    "Datetime" TIMESTAMPTZ PRIMARY KEY,
    "PartOfDay" VARCHAR(20) NOT NULL CHECK ("PartOfDay" IN ('Morning', 'Lunch', 'Afternoon', 'Dinner', 'Night')),
    "Season" VARCHAR(20) NOT NULL CHECK ("Season" IN ('Fall', 'Winter', 'Spring', 'Summer')),
    "WeekNumber" INT NOT NULL CHECK ("WeekNumber" BETWEEN 1 AND 53),
    "DayOfWeek" VARCHAR(20) NOT NULL,
    "CreatedAt" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "UpdatedAt" TIMESTAMPTZ NOT NULL DEFAULT NOW());

CREATE INDEX "IdxCalendarDatetime" ON "Calendar" ("Datetime");
CREATE INDEX "IdxCalendarPartOfDay" ON "Calendar" ("PartOfDay");

-- Forecast
CREATE TABLE "Forecast" (
    "Id" BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "Provider" VARCHAR(50) NOT NULL,
    "RetrievalDatetime" TIMESTAMPTZ NOT NULL,
    "Datetime" TIMESTAMPTZ NOT NULL,
    "CityId" INT NOT NULL REFERENCES "City" ("Id") ON DELETE CASCADE,
    "Temperature" DOUBLE PRECISION,
    "FeltTemperature" DOUBLE PRECISION,
    "Humidity" DOUBLE PRECISION,
    "Visibility" DOUBLE PRECISION,
    "PrecipitationProbability" DOUBLE PRECISION,
    "Rain" DOUBLE PRECISION,
    "Snowfall" DOUBLE PRECISION,
    "CloudCover" DOUBLE PRECISION,
    "WindSpeed" DOUBLE PRECISION,
    "IsCurrent" CHAR(1) NOT NULL CHECK ("IsCurrent" IN ('Y', 'N')),
    "CreatedAt" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "UpdatedAt" TIMESTAMPTZ NOT NULL DEFAULT NOW());

CREATE INDEX "IdxForecastCityDatetime" ON "Forecast" ("CityId", "Datetime");
CREATE INDEX "IdxForecastRetrieval" ON "Forecast" ("Provider", "RetrievalDatetime", "Datetime", "CityId");

-- Actual
CREATE TABLE "Actual" (
    "Id" BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "Provider" VARCHAR(50) NOT NULL,
    "Datetime" TIMESTAMPTZ NOT NULL,
    "CityId" INT NOT NULL REFERENCES "City" ("Id") ON DELETE CASCADE,
    "RetrievalDatetime" TIMESTAMPTZ NOT NULL,
    "Temperature" DOUBLE PRECISION,
    "FeltTemperature" DOUBLE PRECISION,
    "Humidity" DOUBLE PRECISION,
    "Visibility" DOUBLE PRECISION,
    "PrecipitationProbability" DOUBLE PRECISION,
    "Rain" DOUBLE PRECISION,
    "Snowfall" DOUBLE PRECISION,
    "CloudCover" DOUBLE PRECISION,
    "WindSpeed" DOUBLE PRECISION,
    "CreatedAt" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "UpdatedAt" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE ("Datetime", "CityId"));

CREATE INDEX "IdxActualCityDatetime" ON "Actual" ("CityId", "Datetime");

-- StaticEvents
CREATE TABLE "StaticEvents" (
    "Id" BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "Name" VARCHAR(100) NOT NULL,
    "Category" VARCHAR(50) NOT NULL,
    "Cost" VARCHAR(50),
    "IsIndoor" VARCHAR(50) CHECK ("IsIndoor" IN ('Y', 'N', 'Both')),
    "EnergyLevel" VARCHAR(50),
    "SocialLevel" VARCHAR(50),
    "Duration" VARCHAR(50));

-- Forecast Accuracy By Day Span
CREATE TABLE "ForecastAccuracyByDaySpan" (
    "Id" BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "Provider" VARCHAR(50) NOT NULL,
    "DaySpan" INT NOT NULL,
    "Metric" VARCHAR(20) NOT NULL,
    "MAE" DOUBLE PRECISION NOT NULL,
    "MAPE" DOUBLE PRECISION NOT NULL,
    "CreatedAt" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "UpdatedAt" TIMESTAMPTZ NOT NULL DEFAULT NOW());

-- Forecast Accuracy By Provider
CREATE TABLE "ForecastAccuracyByProvider" (
    "Id" BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "Provider" VARCHAR(50) NOT NULL,
    "Metric" VARCHAR(20) NOT NULL,
    "MAE" DOUBLE PRECISION NOT NULL,
    "MAPE" DOUBLE PRECISION NOT NULL,
    "CreatedAt" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "UpdatedAt" TIMESTAMPTZ NOT NULL DEFAULT NOW());

-- Visit Events (Streamlit Analytics)
CREATE TABLE "VisitEvents" (
    "Id" BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "EventTs" TIMESTAMPTZ NOT NULL,
    "VisitId" UUID NOT NULL,
    "SessionId" VARCHAR(100) NOT NULL,
    "EventType" VARCHAR(50) NOT NULL,
    "Page" VARCHAR(50) NOT NULL,
    "AppVersion" VARCHAR(30),
    "UserAgent" TEXT,
    "Referrer" TEXT,
    "IpHash" VARCHAR(128),
    "QueryParams" JSONB NOT NULL DEFAULT '{}'::jsonb,
    "HeadersSample" JSONB NOT NULL DEFAULT '{}'::jsonb,
    "Payload" JSONB NOT NULL DEFAULT '{}'::jsonb,
    "SessionStartedAt" TIMESTAMPTZ,
    "SessionElapsedSeconds" INT,
    "CreatedAt" TIMESTAMPTZ NOT NULL DEFAULT NOW());

CREATE INDEX "IdxVisitEventsEventTs"   ON "VisitEvents" ("EventTs");
CREATE INDEX "IdxVisitEventsVisitId"   ON "VisitEvents" ("VisitId");
CREATE INDEX "IdxVisitEventsEventType" ON "VisitEvents" ("EventType");
CREATE INDEX "IdxVisitEventsPage"      ON "VisitEvents" ("Page");