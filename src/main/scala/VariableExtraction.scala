import org.apache.hadoop.yarn.webapp.hamlet.HamletSpec.COL
import org.apache.spark.sql.SparkSession

//import org.apache.spark.{SparkContext, SparkConf}

object VariableExtraction {
  def main(args: Array[String]) {
    val spark = SparkSession
      .builder()
      .appName("VariableExtraction")
      .getOrCreate()
    import spark.implicits._

    val tankers = spark.read.text("2014_tankers.txt")
    tankers.cache()
    val messages = spark.read.text("../ais/06/12-16.txt")
    //messages = messages.filter(messages.col("_c0").startsWith("!"))
    //messages = messages.filter(messages.col("_c5").startsWith("1"))
    var position_reports = messages.map(row => toPositionReport(row.toString()))
    position_reports = position_reports.filter(p => p.mmsi != "-1")
    val position_reports2 = position_reports.join(tankers, position_reports("mmsi") === tankers("value"))
    println(position_reports2.show())
    //position_reports2.coalesce(1).write.format("com.databricks.spark.csv").option("header", "true").save("ships.csv")
  }

  def toPositionReport(message: String): PositionReport = {
    //println(message)
    val fields = convert1(message).split(",")
    if (fields.length == 8) {
      PositionReport(fields(0), fields(1).toInt, fields(2).toFloat, fields(3).toFloat, fields(4).toFloat,
        fields(5).toFloat, fields(6).toFloat, fields(7).toInt)
    } else {
      PositionReport("-1", 0, 0, 0, 0, 0, 0, 0)
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

  case class PositionReport(mmsi: String, nav_status: Int, rot: Float, sog: Float, lat: Float, lng: Float, cog: Float, utc_sec: Int)
