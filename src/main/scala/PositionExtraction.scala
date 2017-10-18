/**
 * Created by wesselklijnsma on 06-10-17.
 */

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

object PositionExtraction {
  def main(args: Array[String]) {
    val spark = SparkSession
      .builder()
      .appName("PositionExtraction")
      .getOrCreate()
    import spark.implicits._
    val tankers = spark.read.text("tankers_full.txt")
    tankers.cache()

    val messages = spark.read.text("../ais/*").withColumn("date", input_file_name)
    val messages2 = messages.select(substring(col("date"), 46, 10).as("date"), col("value"))
    var position_reports = messages2.map(row => toPositionReport(row.getAs[String]("value"), row.getAs[String]("date")))
    position_reports = position_reports.filter(p => p.mmsi != "-1")
    val position_reports2 = position_reports.join(tankers, position_reports("mmsi") === tankers("value"))
    position_reports2.repartition(4)
    val position_aggregated = position_reports2.groupBy($"date", $"mmsi").agg(avg("lat"), avg("lng"), avg("cog"), avg("sog"))
//    println(position_aggregated.show())
//    position_aggregated.coalesce(1).write.format("com.databricks.spark.csv").option("header", "true").save("pos_agg.csv")
    position_aggregated.write.format("com.databricks.spark.csv").option("header", "true").save("pos_agg_course.csv")
  }


  def toPositionReport(message: String, date: String): PositionReport = {
    //try message1
    var fields = convert1(message).split(",")
    //try message2
    if(fields(0) == "-1"){
      fields = convert2(message).split(",")
      if(fields(0) == "-1"){
        fields = convert3(message).split(",")
      }
    }
    if (fields.length == 8) {
      PositionReport(fields(0), fields(1).toInt, fields(2).toFloat, fields(3).toFloat, fields(4).toFloat,
        fields(5).toFloat, fields(6).toFloat, fields(7).toInt, date)
    } else {
      PositionReport("-1", 0, 0, 0, 0, 0, 0, 0, "-1")
    }
  }

  def convert1(message: String): String = {
    val mes1: Message1 = new Message1()
    val vdmmes: Vdm = new Vdm()
    try {
      if (vdmmes.add(message) == 0) {
        mes1.parse(vdmmes.sixbit())
        mes1.toCsv
      } else {
        "-1,0,0,0,0,0,0,0"
      }
    } catch {
      case e: Exception => "-1,0,0,0,0,0,0,0"
    }
  }

  def convert2(message: String): String = {
    val mes2: Message2 = new Message2()
    val vdmmes: Vdm = new Vdm()
    try {
      if (vdmmes.add(message) == 0) {
        mes2.parse(vdmmes.sixbit())
        mes2.toCsv
      } else {
        "-1,0,0,0,0,0,0,0"
      }
    } catch {
      case e: Exception => "-1,0,0,0,0,0,0,0"
    }
  }

  def convert3(message: String): String = {
    val mes3: Message3 = new Message3()
    val vdmmes: Vdm = new Vdm()
    try {
      if (vdmmes.add(message) == 0) {
        mes3.parse(vdmmes.sixbit())
        mes3.toCsv
      } else {
        "-1,0,0,0,0,0,0,0"
      }
    } catch {
      case e: Exception => "-1,0,0,0,0,0,0,0"
    }
  }
}

//case class PositionReport(mmsi: String, nav_status: Int, rot: Float, sog: Float, lat: Float, lng: Float, cog: Float, utc_sec: Int, date: String)//

