import Tooltip from './tooltip'


/**
 * --------------------------------------------------------------------------
 * Bootstrap (v4.0.0-alpha.2): popover.js
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * --------------------------------------------------------------------------
 */

const Popover = (($) => {


  /**
   * ------------------------------------------------------------------------
   * Constants
   * ------------------------------------------------------------------------
   */

  const NAME                = 'popover'
  const VERSION             = '4.0.0-alpha'
  const DATA_KEY            = 'bs.popover'
  const EVENT_KEY           = `.${DATA_KEY}`
  const JQUERY_NO_CONFLICT  = $.fn[NAME]

  const Default = $.extend({}, Tooltip.Default, {
    placement : 'right',
    trigger   : 'click',
    content   : '',
    template  : '<div class="popover" role="tooltip">'
              + '<div class="popover-arrow"></div>'
              + '<h3 class="popover-title"></h3>'
              + '<div class="popover-content"></div></div>'
  })

  const DefaultType = $.extend({}, Tooltip.DefaultType, {
    content : '(string|element|function)'
  })

  const ClassName = {
    FADE : 'fade',
    IN  : 'in'
  }

  const Selector = {
    TITLE   : '.popover-title',
    CONTENT : '.popover-content',
    ARROW   : '.popover-arrow'
  }

  const Event = {
    HIDE       : `hide${EVENT_KEY}`,
    HIDDEN     : `hidden${EVENT_KEY}`,
    SHOW       : `show${EVENT_KEY}`,
    SHOWN      : `shown${EVENT_KEY}`,
    INSERTED   : `inserted${EVENT_KEY}`,
    CLICK      : `click${EVENT_KEY}`,
    FOCUSIN    : `focusin${EVENT_KEY}`,
    FOCUSOUT   : `focusout${EVENT_KEY}`,
    MOUSEENTER : `mouseenter${EVENT_KEY}`,
    MOUSELEAVE : `mouseleave${EVENT_KEY}`
  }


  /**
   * ------------------------------------------------------------------------
   * Class Definition
   * ------------------------------------------------------------------------
   */

  class Popover extends Tooltip {


    // getters

    static get VERSION() {
      return VERSION
    }

    static get Default() {
      return Default
    }

    static get NAME() {
      return NAME
    }

    static get DATA_KEY() {
      return DATA_KEY
    }

    static get Event() {
      return Event
    }

    static get EVENT_KEY() {
      return EVENT_KEY
    }

    static get DefaultType() {
      return DefaultType
    }


    // overrides

    isWithContent() {
      return this.getTitle() || this._getContent()
    }

    getTipElement() {
      return (this.tip = this.tip || $(this.config.template)[0])
    }

    setContent() {
      let $tip = $(this.getTipElement())

      // we use append for html objects to maintain js events
      this.setElementContent($tip.find(Selector.TITLE), this.getTitle())
      this.setElementContent($tip.find(Selector.CONTENT), this._getContent())

      $tip
        .removeClass(ClassName.FADE)
        .removeClass(ClassName.IN)

      this.cleanupTether()
    }

    // private

    _getContent() {
      return this.element.getAttribute('data-content')
        || (typeof this.config.content === 'function' ?
              this.config.content.call(this.element) :
              this.config.content)
    }


    // static

    static _jQueryInterface(config) {
      return this.each(function () {
        let data   = $(this).data(DATA_KEY)
        let _config = typeof config === 'object' ? config : null

        if (!data && /destroy|hide/.test(config)) {
          return
        }

        if (!data) {
          data = new Popover(this, _config)
          $(this).data(DATA_KEY, data)
        }

        if (typeof config === 'string') {
          if (data[config] === undefined) {
            throw new Error(`No method named "${config}"`)
          }
          data[config]()
        }
      })
    }
  }


  /**
   * ------------------------------------------------------------------------
   * jQuery
   * ------------------------------------------------------------------------
   */

  $.fn[NAME]             = Popover._jQueryInterface
  $.fn[NAME].Constructor = Popover
  $.fn[NAME].noConflict  = function () {
    $.fn[NAME] = JQUERY_NO_CONFLICT
    return Popover._jQueryInterface
  }

  return Popover

})(jQuery)

export default Popover
