resource "kubernetes_ingress" "truelayer-ingress" {
  metadata {
    name      = "truelayer-ingress"
    namespace = "truelayer"
  }
  spec {
    rule {
      host = "pokemon.truelayer.com"
      http {
        path {
          backend {
            service_name = "truelayer-python-services"
            service_port = 80
          }
          path = "/"
        }
      }
    }
  }
  depends_on = [kubernetes_service.truelayer-python-services]
}