from .utils import log_action


def native_font(font):
    log_action('font', 'native_font', font=font)


def measure_text(font, text, tight=False):
    log_action('font', 'measure_text', text=text, tight=tight)
