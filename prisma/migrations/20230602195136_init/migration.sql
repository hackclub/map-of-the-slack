-- CreateTable
CREATE TABLE "Channels" (
    "id" SERIAL NOT NULL,
    "channelID" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "topic" TEXT NOT NULL,
    "members" INTEGER NOT NULL,
    "tag" TEXT,

    CONSTRAINT "Channels_pkey" PRIMARY KEY ("id")
);
