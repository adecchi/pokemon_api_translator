resource "helm_release" "prometheus" {
  name       = "prometheus"
  repository = "https://charts.helm.sh/stable"
  chart      = "prometheus"
  namespace  = "monitoring"
}
