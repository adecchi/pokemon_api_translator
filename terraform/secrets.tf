resource "kubernetes_secret" "influxdb-secrets" {
  metadata {
    name      = "influxdb-secrets"
    namespace = "monitoring"
  }
  data = {
    INFLUXDB_DATABASE = "local_monitoring"
    INFLUXDB_USERNAME = "admin"
    INFLUXDB_PASSWORD = "admin"
    INFLUXDB_HOST     = "influxdb"
  }
}

resource "kubernetes_secret" "grafana-secrets" {
  metadata {
    name      = "grafana-secrets"
    namespace = "monitoring"
  }
  data = {
    GF_SECURITY_ADMIN_USER     = "admin"
    GF_SECURITY_ADMIN_PASSWORD = "admin"
  }
}

resource "kubernetes_secret" "telegraf-secrets" {
  metadata {
    name      = "telegraf-secrets"
    namespace = "monitoring"
  }
  data = {
    INFLUXDB_DB : "local_monitoring"
    INFLUXDB_URL : "http://influxdb:8086"
    INFLUXDB_USER : "admin"
    INFLUXDB_USER_PASSWORD : "admin"
  }
}