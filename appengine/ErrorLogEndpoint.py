
import datetime
import time
import webapp2
from google.appengine.api.logservice import logservice
from google.appengine.api import mail


class ErrorLogEndpoint(webapp2.RequestHandler):
    """
    Sends emails with recent errors. Gratefully adapted from http://stackoverflow.com/a/21655135/1567183.
    """

    def get(self):
        end_time = time.time()
        start_time = end_time - 6 * 60 * 60  # 6 hours before now- same as cronjob interval.
        html = ''
        report_needed = False
        for req_log in logservice.fetch(start_time=start_time, end_time=end_time,
                                        minimum_log_level=logservice.LOG_LEVEL_ERROR, include_app_logs=True):
            report_needed = True
            html += '%s - %s <br/>\n' % (req_log.resource, req_log.method)
            html += '%s <br/>\n' % req_log.ip
            html += '<br/>\n'

            for app_log in req_log.app_logs:
                html += 'Date: %s' % datetime.datetime.fromtimestamp(app_log.time).strftime('%D %T UTC')
                html += '<b><pre>%s</pre></b><br/>\n' % app_log.message

            html += '<hr>\n'

        if report_needed:
            mail.send_mail(sender="nic@snapchat.com",
                           to='nic@snapchat.com',
                           subject='Whaler Errors',
                           body=html,
                           html=html)
        self.response.out.write(html)
