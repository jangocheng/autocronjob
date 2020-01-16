# -*- coding:utf-8 -*-


def msg(taskname, result):
    return """
        <html>
          <head>
              <meta http-equiv="Content-Type" content="text/html; charset=utf-8">

              <style>
              caption {
                  font-size: larger;
                  margin: 1em auto;
                  };

              .th-v1 {
              padding: .65em;
              }

              .th-v1 {
                  background: #555 nonerepeat scroll 0 0;
                  border: 1px solid #777;

              }

              .td-v1 {
                  border: 1px solid#777;
                  padding: .65em;
                  font-family: SimSun;
              }
          </style>

          </head>

          <body style="word-wrap: break-word; -webkit-nbsp-mode: space; line-break: after-white-space;">
              <div><br>
                      <table border="0" cellpadding="0" cellspacing="0" id="body" bgcolor="#fafafa" style="caret-color: rgb(0, 0, 0); font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; font-size: 12px; font-style: normal; font-variant-caps: normal; font-weight: normal; letter-spacing: normal; text-align: center; text-indent: 0px; text-transform: none; white-space: normal; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(250, 250, 250); text-decoration: none; min-width: 640px; width: 720px; margin: 0px; padding: 0px; margin: 0 auto;">
                          <tbody>
                              <tr class="line">
                                  <td bgcolor="#3c8dbc" style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; height: 4px; font-size: 4px; line-height: 4px;">
                                      &nbsp;</td>
                              </tr>
                              <tr class="header">
                                  <td style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; font-size: 13px; line-height: 1.6; color: rgb(92, 92, 92); padding: 25px 0px;">
                                      <img alt="Horizon" src="http://mirrors.hobot.cc/public/horizon/icon.png" width="55" height="50"></td>
                              </tr>
                              <tr>
                                  <td style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif;">
                                      <table border="0" cellpadding="0" cellspacing="0" class="wrapper" style="width: 640px; border-collapse: separate; border-spacing: 0px; margin: 0px auto;">
                                          <tbody>
                                              <tr>
                                                  <td align="left" bgcolor="#ffffff" style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; border-top-left-radius: 3px; border-top-right-radius: 3px; border-bottom-right-radius: 3px; border-bottom-left-radius: 3px; overflow: hidden; padding: 18px 25px; border: 1px solid rgb(237, 237, 237);">
                                                      <table border="0" cellpadding="0" cellspacing="0" class="content" style="width: 588px; border-collapse: separate; border-spacing: 0px;">
                                                          <tbody>
                                                              <tr>
                                                                  <td align="center" style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; color: rgb(51, 51, 51); font-size: 15px; font-weight: 400; line-height: 1.4; padding: 15px 5px;">
                                                                      <div id="content">
                                                                          <h1 align="centor" style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; color: rgb(51, 51, 51); font-size: 18px; font-weight: 400; line-height: 1.4; margin: 0px; padding: 0px;">
                                                                              您好，autocronjob告警</h1>
                                                                              <p>执行 %s 任务异常, 详细信息如下。</p>
                                                                    <div postion: "absoulute" style="word-wrap:break-word;width:700px"><pre>%s</pre></div>
                                              </tr>
                                          </tbody>
                                      </table>
                                  </td>
                              </tr>
                              <tr class="footer">
                                  <td style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; font-size: 13px; line-height: 1.6; color: rgb(92, 92, 92); padding: 25px 0px;">
                                      <img alt="GitLab" height="33" src="http://mirrors.hobot.cc/public/horizon/icon+title.png" width="90" style="display: block; margin: 0px auto 1em;">
                                      <div style="text-align: center">此邮件为autocronjob系统自动发送，请勿回复。<span class="Apple-converted-space">&nbsp;</span></div>
                                  </td>
                              </tr>
                          </tbody>
                   </table>   
              </div>
              <br>
          </body>
          </html>
    """ % (taskname, result)
