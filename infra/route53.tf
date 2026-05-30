data "aws_route53_zone" "main" {
    name = "${var.domain_name}."
    private_zone = false
}

resource "aws_route53_record" "frontend_alias" {
    zone_id = data.aws_route53_zone.main.zone_id
    name = "${var.project}.${var.domain_name}"
    type = "A"

    alias {
        name = aws_cloudfront_distribution.frontend.domain_name
        zone_id = aws_cloudfront_distribution.frontend.hosted_zone_id
        evaluate_target_health = false
    }
}

resource "aws_route53_record" "backend_alias" {
    zone_id = data.aws_route53_zone.main.zone_id
    name = "api.${var.project}.${var.domain_name}"
    type = "A"
    ttl = 300
    records = [aws_eip.django.public_ip]
}