from odoo import http

class Members(http.Controller):

    @http.route("/smth")
    def member_list(self, **kwargs):

        Member = http.request.env["library.member"]
        
        members = Member.search([])
        for member in members:
            print(member.id)


        return http.request.render(
            "library_member.member_list_template",
            {"members": members}
        )
