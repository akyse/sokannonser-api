from flask_restplus import Resource
from jobtech.common.rest.decorators import check_api_key
from sokannonser import settings
from sokannonser.rest import ns_auranest
from sokannonser.rest.model.queries import auranest_query, auranest_typeahead
from sokannonser.rest.model.auranest_results import auranest_lista
from sokannonser.repository import auranest


@ns_auranest.route('search')
class AuranestSearch(Resource):
    method_decorators = [check_api_key('all')]

    @ns_auranest.doc(description='Search with freetext query')
    @ns_auranest.expect(auranest_query)
    def get(self):
        args = auranest_query.parse_args()
        return self.marshal_default(auranest.find_annonser(args))

    @ns_auranest.marshal_with(auranest_lista)
    def marshal_default(self, results):
        return results


@ns_auranest.route('complete')
class AuranestComplete(Resource):
    method_decorators = [check_api_key('all')]

    @ns_auranest.doc(description='Typeahead / Suggest the next search term')
    @ns_auranest.expect(auranest_typeahead)
    def get(self):
        args = auranest_typeahead.parse_args()
        return auranest.autocomplete(args.get(settings.FREETEXT_QUERY))
