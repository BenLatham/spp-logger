import immutables
from helpers import parse_log_lines


def test_logger(spp_logger, log_stream):
    spp_logger.info("my info log message")
    log_messages = parse_log_lines(log_stream.getvalue())
    assert len(log_messages) == 1
    assert log_messages[0]["description"] == "my info log message"


def test_logger_set_context_attribute(spp_logger, log_stream):
    # assert spp_logger.spp_handler.context.get("my_attribute") is None
    spp_logger.set_context_attribute("my_attribute", "my_attribute_value")
    # assert (
    #     spp_logger.spp_handler.context.get("my_attribute") == "my_attribute_value"
    # )
    spp_logger.info("my info log message")
    log_messages = parse_log_lines(log_stream.getvalue())
    assert len(log_messages[0]) == 11
    assert log_messages[0]["my_attribute"] == "my_attribute_value"


def test_context_can_be_overridden(spp_logger, log_stream):
    spp_logger.set_context(immutables.Map(
        log_correlation_id="test", log_level_conf="DEBUG"
    ))
    spp_logger.info("my first log message")
    spp_logger.set_context(immutables.Map(
        log_correlation_id="other test", log_level_conf="INFO"
    ))
    spp_logger.info("my second log message")
    log_messages = parse_log_lines(log_stream.getvalue())
    assert log_messages[0]["log_correlation_id"] == "test"
    assert log_messages[0]["log_level_conf"] == "DEBUG"
    assert log_messages[1]["log_correlation_id"] == "other test"
    assert log_messages[1]["log_level_conf"] == "INFO"
