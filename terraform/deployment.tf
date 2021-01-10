resource "kubernetes_deployment" "truelayer-webserver" {
  metadata {
    name = "truelayer-webserver"
    labels = {
      app     = "WebserverApp"
      version = "v1.0"
    }
    namespace = "truelayer"
  }

  spec {
    replicas = 3
    selector {
      match_labels = {
        app = "WebserverApp"
      }
    }
    template {
      metadata {
        labels = {
          app     = "WebserverApp"
          version = "v1.0"
        }
      }
      spec {
        container {
          image = "adecchi/truelayer:v1.0"
          name  = "python-webserver-image"
          liveness_probe {
            http_get {
              path = "/status"
              port = 8000
            }
            initial_delay_seconds = 5
            period_seconds        = 10
            failure_threshold     = 2
          }
          readiness_probe {
            http_get {
              path = "/status"
              port = 8000
            }
            period_seconds    = 1
            failure_threshold = 1
          }
        }
      }
    }
  }
}

# Grafana
resource "kubernetes_deployment" "grafana" {
  metadata {
    name = "grafana"
    labels = {
      app = "grafana"
    }
    namespace = "monitoring"
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "grafana"
      }
    }
    template {
      metadata {
        labels = {
          app = "grafana"
        }
      }
      spec {
        container {
          image = "docker.io/grafana/grafana:5.3.2"
          name  = "grafana"
          env_from {
            secret_ref {
              name = "grafana-secrets"
            }
          }
        }
      }
    }
  }
  depends_on = [kubernetes_secret.grafana-secrets]
}

# InfluxDB
resource "kubernetes_deployment" "influxdb" {
  metadata {
    name = "influxdb"
    labels = {
      app = "influxdb"
    }
    namespace = "monitoring"
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "influxdb"
      }
    }
    template {
      metadata {
        labels = {
          app = "influxdb"
        }
      }
      spec {
        container {
          image = "docker.io/influxdb:1.6.4"
          name  = "influxdb"
          env_from {
            secret_ref {
              name = "influxdb-secrets"
            }
          }
          volume_mount {
            mount_path = "/var/lib/influxdb"
            name       = "var-lib-influxdb"
          }
        }
        volume {
          name = "var-lib-influxdb"
          persistent_volume_claim {
            claim_name = "influxdb-pvc"
          }
        }
      }
    }
  }
  depends_on = [kubernetes_secret.influxdb-secrets, kubernetes_persistent_volume_claim.influxdb-pvc]
}

# Telegraf
resource "kubernetes_deployment" "telegraf" {
  metadata {
    name = "telegraf"
    labels = {
      app = "telegraf"
    }
    namespace = "monitoring"
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "telegraf"
      }
    }
    template {
      metadata {
        labels = {
          app = "telegraf"
        }
      }
      spec {
        container {
          image = "telegraf:1.10.0"
          name  = "telegraf"
          env_from {
            secret_ref {
              name = "telegraf-secrets"
            }
          }
          volume_mount {
            name       = "telegraf-config-volume"
            mount_path = "/etc/telegraf/telegraf.conf"
            sub_path   = "telegraf.conf"
            read_only  = true
          }
        }
        volume {
          name = "telegraf-config-volume"
          config_map {
            name = "telegraf-config"
          }
        }
      }
    }
  }
  depends_on = [kubernetes_deployment.influxdb, kubernetes_secret.telegraf-secrets, kubernetes_config_map.telegraf-config]
}