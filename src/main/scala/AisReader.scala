import org.apache.spark.sql.SparkSession

object AisReader {

  def main(args: Array[String]) {
    val spark = SparkSession
      .builder()
      .appName("TankerExtraction")
      .getOrCreate()
    import spark.implicits._

    val messages = spark.read.text("/user/hannesm/lsde/ais2/*/*/*")
    var voyage_reports = messages.map(row => toMmsiType(row.toString()))
    voyage_reports = voyage_reports.filter(v => v.mmsi != "-1" && (v.ship_type >= 80 && v.ship_type < 90))
    val tankers = voyage_reports.select(voyage_reports("mmsi")).distinct()
    tankers.write.text("/user/lsde08/tankers_w2017_2.txt")
  }

  def toMmsiType(message: String): MmsiType = {
    val fields = convert5(message).split(",")
    MmsiType(fields(0), fields(1).toInt)
  }


  def convert5(message: String): String = {
    val mes: Message5 = new Message5()
    val vdmmes: Vdm = new Vdm()
    //println(message)
    try {
      if (vdmmes.add(message) == 0) {
        mes.parse(vdmmes.sixbit())
        mes.toCsv
      } else {
        "-1,0"
      }
    } catch {
      case e: Exception => "-1,0"
    }

  }


}

case class MmsiType(mmsi: String, ship_type: Int)
