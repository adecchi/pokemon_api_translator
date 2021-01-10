resource "kubernetes_namespace" "truelayer" {
  metadata {
    name = "truelayer"
  }
}

resource "kubernetes_namespace" "monitoring" {
  metadata {
    name = "monitoring"
  }
}