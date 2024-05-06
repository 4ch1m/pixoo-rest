def create(swagger):
    @swagger.definition('form_param_x')
    class FormParamX:
        """
        Horizontal pixel position.
        ---
        name: x
        in: formData
        type: integer
        minimum: 0
        default: 0
        required: true
        """

    @swagger.definition('form_param_y')
    class FormParamY:
        """
        Vertical pixel position.
        ---
        name: y
        in: formData
        type: integer
        minimum: 0
        default: 0
        required: true
        """

    @swagger.definition('form_param_r')
    class FormParamR:
        """
        RGB - Red color value.
        ---
        name: r
        in: formData
        type: integer
        minimum: 0
        maximum: 255
        default: 255
        required: true
        """

    @swagger.definition('form_param_g')
    class FormParamG:
        """
        RGB - Green color value.
        ---
        name: g
        in: formData
        type: integer
        minimum: 0
        maximum: 255
        default: 255
        required: true
        """

    @swagger.definition('form_param_b')
    class FormParamB:
        """
        RGB - Blue color value.
        ---
        name: b
        in: formData
        type: integer
        minimum: 0
        maximum: 255
        default: 255
        required: true
        """

    @swagger.definition('form_param_push_immediately')
    class FormParamPushImmediately:
        """
        Push draw buffer to the device immediately after this operation?
        ---
        name: push_immediately
        in: formData
        type: boolean
        default: true
        required: true
        """

    @swagger.definition('form_param_timeout')
    class FormParamTimeout:
        """
        Connection timeout in seconds.
        ---
        name: timeout
        in: formData
        type: integer
        minimum: 3
        maximum: 300
        default: 30
        required: true
        """

    @swagger.definition('form_param_ssl_verify')
    class FormParamSslVerify:
        """
        Verify SSL certificates for HTTPS requests.
        ---
        name: ssl_verify
        in: formData
        type: boolean
        default: true
        required: false
        """

    @swagger.definition('form_param_scroll_direction')
    class FormParamScrollDirection:
        """
        The scroll direction.
          * 0 = left
          * 1 = right
        ---
        name: scroll_direction
        in: formData
        type: integer
        enum:
          - 0
          - 1
        default: 0
        required: true
        """

    @swagger.definition('form_param_scroll_speed')
    class FormParamMovementSpeed:
        """
        The scroll speed in milliseconds.
        ---
        name: scroll_speed
        in: formData
        type: integer
        default: 100
        required: true
        """

    @swagger.definition('form_param_text_width')
    class FormParamTextWidth:
        """
        Text width.
        ---
        name: text_width
        in: formData
        type: integer
        minimum: 1
        maximum: 64
        default: 64
        required: true
        """

    @swagger.definition('form_param_text_height')
    class FormParamTextHeight:
        """
        Text height.
        ---
        name: text_height
        in: formData
        type: integer
        minimum: 1
        maximum: 64
        default: 16
        required: true
        """
