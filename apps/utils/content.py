#!/usr/bin/env python
# -*- coding: utf-8 -*-


def examine_body(approver, petitioner, app, redirect):
    return '''
    <html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
</head>

<body style="word-wrap: break-word; -webkit-nbsp-mode: space; line-break: after-white-space;" class="">
    <div><br class="">
            <table border="0" cellpadding="0" cellspacing="0" id="body" bgcolor="#fafafa" style="caret-color: rgb(0, 0, 0); font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; font-size: 12px; font-style: normal; font-variant-caps: normal; font-weight: normal; letter-spacing: normal; text-align: center; text-indent: 0px; text-transform: none; white-space: normal; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(250, 250, 250); text-decoration: none; min-width: 640px; width: 720px; margin: 0px; padding: 0px; margin: 0 auto;"
                class="">
                <tbody class="">
                    <tr class="line">
                        <td bgcolor="#6b4fbb" style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; height: 4px; font-size: 4px; line-height: 4px;" class="">
                            &nbsp;</td>
                    </tr>
                    <tr class="header">
                        <td style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; font-size: 13px; line-height: 1.6; color: rgb(92, 92, 92); padding: 25px 0px;" class="">
                            <img alt="Horizon" src="http://mirrors.hobot.cc/public/horizon/icon.png" width="55" height="50" class=""></td>
                    </tr>
                    <tr class="">
                        <td style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif;" class="">
                            <table border="0" cellpadding="0" cellspacing="0" class="wrapper" style="width: 640px; border-collapse: separate; border-spacing: 0px; margin: 0px auto;">
                                <tbody class="">
                                    <tr class="">
                                        <td align="left" bgcolor="#ffffff" style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; border-top-left-radius: 3px; border-top-right-radius: 3px; border-bottom-right-radius: 3px; border-bottom-left-radius: 3px; overflow: hidden; padding: 18px 25px; border: 1px solid rgb(237, 237, 237);"
                                            class="">
                                            <table border="0" cellpadding="0" cellspacing="0" class="content" style="width: 588px; border-collapse: separate; border-spacing: 0px;">
                                                <tbody class="">
                                                    <tr class="">
                                                        <td align="center" style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; color: rgb(51, 51, 51); font-size: 15px; font-weight: 400; line-height: 1.4; padding: 15px 5px;" class="">
                                                            <div id="content" class="">
                                                                <h1 align="centor" style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; color: rgb(51, 51, 51); font-size: 18px; font-weight: 400; line-height: 1.4; margin: 0px; padding: 0px;" class="">
                                                                    您好，{}</h1>
                                                                <p class=""> 有一个来自<span style="color:red;">{}</span>的<span style="color:0066FF;">{}</span>流程需要您的审批。</p>
                                                                <br/>
                                                                  <div id="cta" class=""><a style="    text-decoration:none;
	                                                                    background:#0066FF;
                                                                        color:#f2f2f2;
                                                                        
                                                                        padding: 10px 30px 10px 30px;
                                                                        font-size:16px;
                                                                        font-family: 微软雅黑,宋体,Arial,Helvetica,Verdana,sans-serif;
                                                                        font-weight:bold;
                                                                        border-radius:3px;
                                                                        
                                                                        -webkit-transition:all linear 0.30s;
                                                                        -moz-transition:all linear 0.30s;
                                                                        transition:all linear 0.30s;
！" href="{}" class="">审批该请求</a></div>
                                                            </div>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </td>
                    </tr>
                    <tr class="footer">
                        <td style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; font-size: 13px; line-height: 1.6; color: rgb(92, 92, 92); padding: 25px 0px;" class="">
                            <img alt="GitLab" height="33" src="http://mirrors.hobot.cc/public/horizon/icon+title.png" width="90" style="display: block; margin: 0px auto 1em;" class="">
                                <div class="">此邮件为地平线工单系统自动发送，请勿回复。<span class="Apple-converted-space">&nbsp;</span></div>
                        </td>
                    </tr>
                </tbody>
            </table>
    </div>
    <br class="">
</body>
</html>
'''.format(approver, petitioner, app, redirect)


def refuse_body(petitioner, message, redirect):
    return '''
      <html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
</head>

<body style="word-wrap: break-word; -webkit-nbsp-mode: space; line-break: after-white-space;" class="">
    <div><br class="">
            <table border="0" cellpadding="0" cellspacing="0" id="body" bgcolor="#fafafa" style="caret-color: rgb(0, 0, 0); font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; font-size: 12px; font-style: normal; font-variant-caps: normal; font-weight: normal; letter-spacing: normal; text-align: center; text-indent: 0px; text-transform: none; white-space: normal; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(250, 250, 250); text-decoration: none; min-width: 640px; width: 720px; margin: 0px; padding: 0px; margin: 0 auto;"
                class="">
                <tbody class="">
                    <tr class="line">
                        <td bgcolor="##0066FF" style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; height: 4px; font-size: 4px; line-height: 4px;" class="">
                            &nbsp;</td>
                    </tr>
                    <tr class="header">
                        <td style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; font-size: 13px; line-height: 1.6; color: rgb(92, 92, 92); padding: 25px 0px;" class="">
                            <img alt="Horizon" src="http://mirrors.hobot.cc/public/horizon/icon.png" width="55" height="50" class=""></td>
                    </tr>
                    <tr class="">
                        <td style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif;" class="">
                            <table border="0" cellpadding="0" cellspacing="0" class="wrapper" style="width: 640px; border-collapse: separate; border-spacing: 0px; margin: 0px auto;">
                                <tbody class="">
                                    <tr class="">
                                        <td align="left" bgcolor="#ffffff" style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; border-top-left-radius: 3px; border-top-right-radius: 3px; border-bottom-right-radius: 3px; border-bottom-left-radius: 3px; overflow: hidden; padding: 18px 25px; border: 1px solid rgb(237, 237, 237);"
                                            class="">
                                            <table border="0" cellpadding="0" cellspacing="0" class="content" style="width: 588px; border-collapse: separate; border-spacing: 0px;">
                                                <tbody class="">
                                                    <tr class="">
                                                        <td align="center" style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; color: rgb(51, 51, 51); font-size: 15px; font-weight: 400; line-height: 1.4; padding: 15px 5px;" class="">
                                                            <div id="content" class="">
                                                                <h1 align="centor" style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; color: rgb(51, 51, 51); font-size: 18px; font-weight: 400; line-height: 1.4; margin: 0px; padding: 0px;" class="">
                                                                    您好，{}</h1>
                                                                <p class="" style="color: red;">您的请求被拒绝了，详细信息如下。</p>
                                                                <p>{}</p>
                                                                 <br/>
                                                                  <div id="cta" class=""><a style="    text-decoration:none;
	                                                                    background:#0066FF;
                                                                        color:#f2f2f2;
                                                                        
                                                                        padding: 10px 30px 10px 30px;
                                                                        font-size:16px;
                                                                        font-family: 微软雅黑,宋体,Arial,Helvetica,Verdana,sans-serif;
                                                                        font-weight:bold;
                                                                        border-radius:3px;
                                                                        
                                                                        -webkit-transition:all linear 0.30s;
                                                                        -moz-transition:all linear 0.30s;
                                                                        transition:all linear 0.30s;
！" href="{}" class="">查看详情</a></div>
                                                            </div>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </td>
                    </tr>
                    <tr class="footer">
                        <td style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; font-size: 13px; line-height: 1.6; color: rgb(92, 92, 92); padding: 25px 0px;" class="">
                            <img alt="GitLab" height="33" src="http://mirrors.hobot.cc/public/horizon/icon+title.png" width="90" style="display: block; margin: 0px auto 1em;" class="">
                                <div class="">此邮件为地平线工单系统自动发送，请勿回复。<span class="Apple-converted-space">&nbsp;</span></div>
                        </td>
                    </tr>
                </tbody>
            </table>
    </div>
    <br class="">
</body>
</html>
    '''.format(petitioner, message, redirect)


def result_body(data, recv):
    return '''
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

    <body style="word-wrap: break-word; -webkit-nbsp-mode: space; line-break: after-white-space;" class="">
        <div><br class="">
                <table border="0" cellpadding="0" cellspacing="0" id="body" bgcolor="#fafafa" style="caret-color: rgb(0, 0, 0); font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; font-size: 12px; font-style: normal; font-variant-caps: normal; font-weight: normal; letter-spacing: normal; text-align: center; text-indent: 0px; text-transform: none; white-space: normal; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(250, 250, 250); text-decoration: none; min-width: 640px; width: 720px; margin: 0px; padding: 0px; margin: 0 auto;"
                    class="">
                    <tbody class="">
                        <tr class="line">
                            <td bgcolor="#0066FF" style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; height: 4px; font-size: 4px; line-height: 4px;" class="">
                                &nbsp;</td>
                        </tr>
                        <tr class="header">
                            <td style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; font-size: 13px; line-height: 1.6; color: rgb(92, 92, 92); padding: 25px 0px;" class="">
                                <img alt="Horizon" src="http://mirrors.hobot.cc/public/horizon/icon.png" width="55" height="50" class=""></td>
                        </tr>
                        <tr class="">
                            <td style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif;" class="">
                                <table border="0" cellpadding="0" cellspacing="0" class="wrapper" style="width: 640px; border-collapse: separate; border-spacing: 0px; margin: 0px auto;">
                                    <tbody class="">
                                        <tr class="">
                                            <td align="left" bgcolor="#ffffff" style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; border-top-left-radius: 3px; border-top-right-radius: 3px; border-bottom-right-radius: 3px; border-bottom-left-radius: 3px; overflow: hidden; padding: 18px 25px; border: 1px solid rgb(237, 237, 237);"
                                                class="">
                                                <table border="0" cellpadding="0" cellspacing="0" class="content" style="width: 588px; border-collapse: separate; border-spacing: 0px;">
                                                    <tbody class="">
                                                        <tr class="">
                                                            <td align="center" style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; color: rgb(51, 51, 51); font-size: 15px; font-weight: 400; line-height: 1.4; padding: 15px 5px;" class="">
                                                                <div id="content" class="">
                                                                    <h1 align="centor" style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; color: rgb(51, 51, 51); font-size: 18px; font-weight: 400; line-height: 1.4; margin: 0px; padding: 0px;" class="">
                                                                        您好，%s</h1>
                                                                        <p>您的请求已受理完毕, 详细信息如下。</p>
                                                                  <table style="border-collapse: collapse;font-family: Futura, Arial, sans-serif;">
                                                                <tr>
                                                                    <th class="th-v1">IP地址</th>
                                                                    <th class="th-v1">主机名称</th>
                                                                    <th class="th-v1">账号</th>
                                                                    <th class="th-v1">密码</th>
                                                                    <th class="th-v1">版本</th>
                                                                    <th class="th-v1">CPU</th>
                                                                    <th class="th-v1">内存</th>
                                                                    <th class="th-v1">磁盘</th>
                                                                </tr>
                                                                <tr>
                                                                    <td class="td-v1">%s</td>
                                                                    <td class="td-v1">%s</td>
                                                                    <td class="td-v1">%s</td>
                                                                    <td class="td-v1">%s</td>
                                                                    <td class="td-v1">%s</td>
                                                                    <td class="td-v1">%s</td>
                                                                    <td class="td-v1">%s</td>
                                                                    <td class="td-v1">%s</td>
                                                                </tr>

                                                        </div>
                                                    </td>
                                                </tr>

                                                </table>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </td>
                        </tr>
                        <tr class="footer">
                            <td style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; font-size: 13px; line-height: 1.6; color: rgb(92, 92, 92); padding: 25px 0px;" class="">
                                <img alt="GitLab" height="33" src="http://mirrors.hobot.cc/public/horizon/icon+title.png" width="90" style="display: block; margin: 0px auto 1em;" class="">
                                <div class="" style="text-align: center">此邮件为地平线工单系统自动发送，请勿回复。<span class="Apple-converted-space">&nbsp;</span></div>
                            </td>
                        </tr>
                    </tbody>
             </table>   
        </div>
        <br class="">
    </body>
    </html>
    '''% (recv, data['ip'],
               data['name'],
              data['username'],
              data['password'],
              data['version'],
              data['vcpu'],
              data['ram'],
              data['disk'])


def get_captcha_style(username, captcha):
    return '''
    <html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
</head>

<body style="word-wrap: break-word; -webkit-nbsp-mode: space; line-break: after-white-space;" class="">
    <div><br class="">
            <table border="0" cellpadding="0" cellspacing="0" id="body" bgcolor="#fafafa" style="caret-color: rgb(0, 0, 0); font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; font-size: 12px; font-style: normal; font-variant-caps: normal; font-weight: normal; letter-spacing: normal; text-align: center; text-indent: 0px; text-transform: none; white-space: normal; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(250, 250, 250); text-decoration: none; min-width: 640px; width: 720px; margin: 0px; padding: 0px; margin: 0 auto;"
                class="">
                <tbody class="">
                    <tr class="line">
                        <td bgcolor="#6b4fbb" style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; height: 4px; font-size: 4px; line-height: 4px;" class="">
                            &nbsp;</td>
                    </tr>
                    <tr class="header">
                        <td style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; font-size: 13px; line-height: 1.6; color: rgb(92, 92, 92); padding: 25px 0px;" class="">
                            <img alt="Horizon" src="http://mirrors.hobot.cc/public/horizon/icon.png" width="55" height="50" class=""></td>
                    </tr>
                    <tr class="">
                        <td style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif;" class="">
                            <table border="0" cellpadding="0" cellspacing="0" class="wrapper" style="width: 640px; border-collapse: separate; border-spacing: 0px; margin: 0px auto;">
                                <tbody class="">
                                    <tr class="">
                                        <td align="left" bgcolor="#ffffff" style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; border-top-left-radius: 3px; border-top-right-radius: 3px; border-bottom-right-radius: 3px; border-bottom-left-radius: 3px; overflow: hidden; padding: 18px 25px; border: 1px solid rgb(237, 237, 237);"
                                            class="">
                                            <table border="0" cellpadding="0" cellspacing="0" class="content" style="width: 588px; border-collapse: separate; border-spacing: 0px;">
                                                <tbody class="">
                                                    <tr class="">
                                                        <td align="center" style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; color: rgb(51, 51, 51); font-size: 15px; font-weight: 400; line-height: 1.4; padding: 15px 5px;" class="">
                                                            <div id="content" class="">
                                                                <h1 align="centor" style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; color: rgb(51, 51, 51); font-size: 18px; font-weight: 400; line-height: 1.4; margin: 0px; padding: 0px;" class="">
                                                                    您好，{}</h1>
                                                                <p class="">此次重置LDAP账号的验证码为:<span style="color: red">{}</span></p>
                                                                <br/>
                                                                
                                                            </div>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </td>
                    </tr>
                    <tr class="footer">
                        <td style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; font-size: 13px; line-height: 1.6; color: rgb(92, 92, 92); padding: 25px 0px;" class="">
                            <img alt="GitLab" height="33" src="http://mirrors.hobot.cc/public/horizon/icon+title.png" width="90" style="display: block; margin: 0px auto 1em;" class="">
                                <div class="">此邮件为地平线工单系统自动发送，请勿回复。<span class="Apple-converted-space">&nbsp;</span></div>
                        </td>
                    </tr>
                </tbody>
            </table>
    </div>
    <br class="">
</body>
</html>
'''.format(username, captcha)


def ali_oss_html(username, access_key, access_key_securt, bucket_name, region, pub_endpoient, vpc_endpoient):
    return '''
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

       <body style="word-wrap: break-word; -webkit-nbsp-mode: space; line-break: after-white-space;" class="">
           <div><br class="">
                   <table border="0" cellpadding="0" cellspacing="0" id="body" bgcolor="#fafafa" style="caret-color: rgb(0, 0, 0); font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; font-size: 12px; font-style: normal; font-variant-caps: normal; font-weight: normal; letter-spacing: normal; text-align: center; text-indent: 0px; text-transform: none; white-space: normal; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(250, 250, 250); text-decoration: none; min-width: 640px; width: 720px; margin: 0px; padding: 0px; margin: 0 auto;"
                       class="">
                       <tbody class="">
                           <tr class="line">
                               <td bgcolor="#0066FF" style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; height: 4px; font-size: 4px; line-height: 4px;" class="">
                                   &nbsp;</td>
                           </tr>
                           <tr class="header">
                               <td style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; font-size: 13px; line-height: 1.6; color: rgb(92, 92, 92); padding: 25px 0px;" class="">
                                   <img alt="Horizon" src="http://mirrors.hobot.cc/public/horizon/icon.png" width="55" height="50" class=""></td>
                           </tr>
                           <tr class="">
                               <td style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif;" class="">
                                   <table border="0" cellpadding="0" cellspacing="0" class="wrapper" style="width: 640px; border-collapse: separate; border-spacing: 0px; margin: 0px auto;">
                                       <tbody class="">
                                           <tr class="">
                                               <td align="left" bgcolor="#ffffff" style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; border-top-left-radius: 3px; border-top-right-radius: 3px; border-bottom-right-radius: 3px; border-bottom-left-radius: 3px; overflow: hidden; padding: 18px 25px; border: 1px solid rgb(237, 237, 237);"
                                                   class="">
                                                   <table border="0" cellpadding="0" cellspacing="0" class="content" style="width: 588px; border-collapse: separate; border-spacing: 0px;">
                                                       <tbody class="">
                                                           <tr class="">
                                                               <td align="center" style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; color: rgb(51, 51, 51); font-size: 15px; font-weight: 400; line-height: 1.4; padding: 15px 5px;" class="">
                                                                   <div id="content" class="">
                                                                       <h1 align="centor" style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; color: rgb(51, 51, 51); font-size: 18px; font-weight: 400; line-height: 1.4; margin: 0px; padding: 0px;" class="">
                                                                           您好，%s</h1>
                                                                           <p>您的请求已受理完毕, 详细信息如下。</p>
                                                                     <table style="border-collapse: collapse;font-family: Futura, Arial, sans-serif;">
                                                                   <tr>
                                                                        <th class="th-v1">AccessId</th>
                                                                        <th class="th-v1">AccessKey</th>                                              
                                                                        <th class="th-v1">Bucket</th>
                                                                        <th class="th-v1">Region</th>
                                                                        <th class="th-v1">ExtranetEndpoient</th>
                                                                        <th class="th-v1">VpcEndpoient</th>
                                                                      
                                                                      
                                                                   </tr>
                                                                   <tr>
                                                                       <td class="td-v1">%s</td>
                                                                       <td class="td-v1">%s</td>                                                                      
                                                                       <td class="td-v1">%s</td>
                                                                       <td class="td-v1">%s</td>
                                                                       <td class="td-v1"><a href="#">https://%s</a></td>
                                                                       <td class="td-v1"><a href="#">https://%s</a></td>

                                                                       
                                                                   </tr>

                                                           </div>
                                                       </td>
                                                   </tr>

                                                   </table>
                                               </td>
                                           </tr>
                                       </tbody>
                                   </table>
                               </td>
                           </tr>
                           <tr class="footer">
                               <td style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; font-size: 13px; line-height: 1.6; color: rgb(92, 92, 92); padding: 25px 0px;" class="">
                                   <img alt="GitLab" height="33" src="http://mirrors.hobot.cc/public/horizon/icon+title.png" width="90" style="display: block; margin: 0px auto 1em;" class="">
                                   <div class="" style="text-align: center">此邮件为地平线工单系统自动发送，请勿回复。<span class="Apple-converted-space">&nbsp;</span></div>
                               </td>
                           </tr>
                       </tbody>
                </table>   
           </div>
           <br class="">
       </body>
       </html>
       ''' % (username, access_key, access_key_securt, bucket_name, region, pub_endpoient, vpc_endpoient)


def reboot_html(user='zongyang.yu', result=None):
    return '''
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

          <body style="word-wrap: break-word; -webkit-nbsp-mode: space; line-break: after-white-space;" class="">
              <div><br class="">
                      <table border="0" cellpadding="0" cellspacing="0" id="body" bgcolor="#fafafa" style="caret-color: rgb(0, 0, 0); font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; font-size: 12px; font-style: normal; font-variant-caps: normal; font-weight: normal; letter-spacing: normal; text-align: center; text-indent: 0px; text-transform: none; white-space: normal; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(250, 250, 250); text-decoration: none; min-width: 640px; width: 720px; margin: 0px; padding: 0px; margin: 0 auto;"
                          class="">
                          <tbody class="">
                              <tr class="line">
                                  <td bgcolor="#0066FF" style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; height: 4px; font-size: 4px; line-height: 4px;" class="">
                                      &nbsp;</td>
                              </tr>
                              <tr class="header">
                                  <td style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; font-size: 13px; line-height: 1.6; color: rgb(92, 92, 92); padding: 25px 0px;" class="">
                                      <img alt="Horizon" src="http://mirrors.hobot.cc/public/horizon/icon.png" width="55" height="50" class=""></td>
                              </tr>
                              <tr class="">
                                  <td style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif;" class="">
                                      <table border="0" cellpadding="0" cellspacing="0" class="wrapper" style="width: 640px; border-collapse: separate; border-spacing: 0px; margin: 0px auto;">
                                          <tbody class="">
                                              <tr class="">
                                                  <td align="left" bgcolor="#ffffff" style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; border-top-left-radius: 3px; border-top-right-radius: 3px; border-bottom-right-radius: 3px; border-bottom-left-radius: 3px; overflow: hidden; padding: 18px 25px; border: 1px solid rgb(237, 237, 237);"
                                                      class="">
                                                      <table border="0" cellpadding="0" cellspacing="0" class="content" style="width: 588px; border-collapse: separate; border-spacing: 0px;">
                                                          <tbody class="">
                                                              <tr class="">
                                                                  <td align="center" style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; color: rgb(51, 51, 51); font-size: 15px; font-weight: 400; line-height: 1.4; padding: 15px 5px;" class="">
                                                                      <div id="content" class="">
                                                                          <h1 align="centor" style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; color: rgb(51, 51, 51); font-size: 18px; font-weight: 400; line-height: 1.4; margin: 0px; padding: 0px;" class="">
                                                                              您好，%s</h1>
                                                                              <p>您的请求已受理完毕, 详细信息如下。</p>
                                                                    <div postion: "absoulute"><pre>%s</pre></div>
                                              </tr>
                                          </tbody>
                                      </table>
                                  </td>
                              </tr>
                              <tr class="footer">
                                  <td style="font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; font-size: 13px; line-height: 1.6; color: rgb(92, 92, 92); padding: 25px 0px;" class="">
                                      <img alt="GitLab" height="33" src="http://mirrors.hobot.cc/public/horizon/icon+title.png" width="90" style="display: block; margin: 0px auto 1em;" class="">
                                      <div class="" style="text-align: center">此邮件为地平线工单系统自动发送，请勿回复。<span class="Apple-converted-space">&nbsp;</span></div>
                                  </td>
                              </tr>
                          </tbody>
                   </table>   
              </div>
              <br class="">
          </body>
          </html>
          ''' % (user, result)
