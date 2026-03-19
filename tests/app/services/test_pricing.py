from src.app.services.pricing import PricingService

def test_pricing_calculation():
    service = PricingService(base_rate=2.0)
    result = service.calculate_cost(10)
    assert result == 20.0