import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.apache.spark.rdd.RDD

object AisReader {
  def main(args: Array[String]) {
    val conf = new SparkConf().setAppName("AisReader")
    val sc = new SparkContext(conf)

    val aisfile = sc.textFile("/user/hannesm/lsde/ais2/*/*/*")
    val aivdm_messages = aisfile.filter(line => line(0) == '!')
    val voyage_reports = aivdm_messages.map(line => convert5(line))
    //println(voyage_reports.count())
    //val position_reports = aivdm_messages.map(line => convert1(line))
//    val position_header: RDD[String] = sc.parallelize(Array("message_id,repeat,mmsi,nav_status,rot,sog,pos_acc,lat,lng,cog,true_heading," +
//      "utc_sec,regional,spare,raim,sync_state,slot_time_out,sub_message"))
    //position_header.union(position_reports.filter(line => line != " ")).repartition(1).saveAsTextFile("positions.txt")
    val ship_types = voyage_reports.filter(line => line != " ")
    val ship_types1 = ship_types.map(l => mmsi_type_pair(l)).distinct()
    val ship_types2 = ship_types1.filter(t => tanker(t._2))
    ship_types2.map(l=> l._1).saveAsTextFile("/user/lsde08/tankers.txt")
    //scala.io.StdIn.readLine()
  }

  def tanker(t: Int): Boolean = {
    t >= 80 && t < 90
  }

  def mmsi_type_pair(line: String): (String, Int) = {
    val values = line.split(",")
    try {
      (values(2), values(7).toInt)
    } catch {
      case e : Exception => (values(2), 0)
    }
  }


  def convert5(message: String): String = {
    val mes: Message5 = new Message5()
    val vdmmes: Vdm = new Vdm()
    //println(message)
    try {
      if (vdmmes.add(message) == 0 && vdmmes.msgid() == 5) {
        mes.parse(vdmmes.sixbit())
        mes.toCsv
      } else {
        " "
      }
    } catch {
      case e: Exception => " "
    }

  }

}
