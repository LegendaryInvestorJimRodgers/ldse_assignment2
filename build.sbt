name := "lsde_assignment2"

version := "1.0"

scalaVersion := "2.11.8"
javacOptions ++= Seq("-source", "1.7", "-target", "1.7")
libraryDependencies += "org.apache.spark" %% "spark-sql" % "2.2.0"
