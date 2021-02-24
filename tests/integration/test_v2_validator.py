from openapi_spec_validator.exceptions import OpenAPIValidationError


class TestSpecValidatorIterErrors(object):

    def test_parameter_default_value_wrong_type(self, swagger_validator):
        spec = {
            'swagger': '2.0',
            'info': {
                'title': 'Test Api',
                'version': '0.0.1',
            },
            'paths': {
                '/test/': {
                    'get': {
                        'responses': {
                            '200': {
                                'description': 'OK',
                                'schema': {'type': 'object'},
                            },
                        },
                        'parameters': [
                            {
                                'name': 'param1',
                                'in': 'query',
                                'type': 'integer',
                                'default': 'invaldtype',
                            },
                        ],
                    },
                },
            },
        }

        errors = swagger_validator.iter_errors(spec)

        errors_list = list(errors)
        assert len(errors_list) == 1
        assert errors_list[0].__class__ == OpenAPIValidationError
        assert errors_list[0].message == (
            "'invaldtype' is not of type integer"
        )
