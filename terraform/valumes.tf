# Volume for InfluxDB
resource "kubernetes_persistent_volume_claim" "influxdb-pvc" {
  metadata {
    name      = "influxdb-pvc"
    namespace = "monitoring"
    labels = {
      app = "influxdb"
    }
  }
  spec {
    access_modes = ["ReadWriteMany"]
    resources {
      requests = {
        storage = "1Gi"
      }
    }
    volume_name = kubernetes_persistent_volume.influxdb-pv.metadata.0.name
  }
}

resource "kubernetes_persistent_volume" "influxdb-pv" {
  metadata {
    name = "influxdb-pv"
  }
  spec {
    capacity = {
      storage = "2Gi"
    }
    access_modes = ["ReadWriteMany"]
    persistent_volume_source {
      host_path {
        path = "/mnt/vda1/hostpath_pv"
      }
    }
    storage_class_name = "standard"
  }
}
