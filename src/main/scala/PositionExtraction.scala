/**
 * Created by wesselklijnsma on 06-10-17.
 */

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

object PositionExtraction {
  def main(args: Array[String]) {
    val spark = SparkSession
      .builder()
      .appName("VariableExtraction")
      .getOrCreate()
    import spark.implicits._
    val tankers = spark.read.text("2014_tankers.txt")
    tankers.cache()

    val messages = spark.read.text("../ais2/*/*/*").withColumn("date", input_file_name)
    val messages2 = messages.select(substring(col("date"), 68, 10).as("date"), col("value"))
    var position_reports = messages2.map(row => toPositionReport(row.getAs[String]("value"), row.getAs[String]("date")))
    position_reports = position_reports.filter(p => p.mmsi != "-1")
    val position_reports2 = position_reports.join(tankers, position_reports("mmsi") === tankers("value"))
    val position_aggregated = position_reports2.groupBy($"date", $"mmsi").agg(avg("lat"), avg("long"))
    println(position_aggregated.show())


  }
  def toPositionReport(message: String, date: String): PositionReport = {
    //println(message)
    val fields = convert1(message).split(",")
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
}

case class PositionReport(mmsi: String, nav_status: Int, rot: Float, sog: Float, lat: Float, lng: Float, cog: Float, utc_sec: Int, date: String)//

