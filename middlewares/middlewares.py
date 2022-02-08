from firebase_admin import auth

# class TockenDecode:
#     def __init__(self,get_response):
#         self.get_response

#     def __call__(self,request):
#         try:
#             auth_header=request.META.get('HTTP_AUTHORIZATION')
#             tocken=auth_header.replace('Bearer ','')
#             decoded_tocken=auth.verify_id_token(tocken)
#             userid=decoded_tocken['user_id']
#         except:
#             response=self.get_response(request)
#         response=self.get_response(request)
#         return response
    
#     def inject_tocken_data(self,_,response):
#         response.context_data["tocken_decode"]=self.tocken_decode
#         return response

def tocken_decode(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        decoded_tocken=False
        try:
            auth_header=request.META.get('HTTP_AUTHORIZATION')
            tocken=auth_header.replace('Bearer ','')
            decoded_tocken=auth.verify_id_token(tocken)
        except:
            decoded_tocken=False
        
        if decoded_tocken:
            request.tocken=decoded_tocken
        else:
            request.tocken=''

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware
