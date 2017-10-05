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
    var year = 2014
    var month, day = 1
    var dataset = spark.createDataset(Seq(AggregatedSOG))

    while (year <= 2016) {
      while (month <= 12) {
        try {
          while (day <= 31) {
            try {
              val messages = spark.read.text("/user/hannesm/lsde/ais2/" + year + "/" + "%02d".format(month) + "/" + "%02d".format(day))
              var position_reports = messages.map(row => toPositionReport(row.toString()))
              position_reports = position_reports.filter(p => p.mmsi != "-1")
              val position_reports2 = position_reports.join(tankers, position_reports("mmsi") === tankers("value"))
              println(position_reports2.show())
              val sog_aggregated = position_reports2.groupBy($"mmsi").avg("sog")
              println(sog_aggregated.show())
              //position_reports2.coalesce(1).write.format("com.databricks.spark.csv").option("header", "true").save("ships.csv")
              val slow = sog_aggregated.filter($"sog" < 1).count()
              val med = sog_aggregated.filter( $"sog" < 5 && $"sog" >= 1).count()
              val fast = sog_aggregated.filter($"sog" >= 5).count()
              dataset = dataset.union(spark.createDataset(AggregatedSOG(year + "/" + month + "/" + day, slow.toInt, med.toInt, fast.toInt)))
              day += 1
            } catch {
              case e: Exception => day += 1
            }
            month += 1
          }
        } catch {
          case e: Exception => month += 1
        }
        day = 1
      }
      day = 1
      month = 1
      year += 1
    }

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

case class AggregatedSOG(date: String, slow: Int, med: Int, fast: Int)