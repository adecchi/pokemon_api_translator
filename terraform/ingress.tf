resource "kubernetes_ingress" "truelayer-ingress" {
  metadata {
    name      = "truelayer-ingress"
    namespace = "truelayer"
    annotations = {
      "nginx.ingress.kubernetes.io/limit-rps" : 5
      "nginx.ingress.kubernetes.io/proxy-buffering" : "on"
      "nginx.ingress.kubernetes.io/configuration-snippet" : <<EOF
          proxy_cache auth_cache;
          proxy_cache_valid 200 1m;
          proxy_cache_use_stale error timeout updating http_404 http_500 http_502 http_503 http_504;
          proxy_cache_bypass $http_x_purge;
          proxy_ignore_headers Cache-Control;
          add_header X-Cache-Status $upstream_cache_status;
          EOF
    }
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