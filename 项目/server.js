const http = require('http');
const fs = require('fs');
const url = require('url');
const querystring = require('querystring');

const port = 8080;
const hostname = '127.0.0.1';

// 简单的会话存储
let sessions = {};

const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url);
    const pathname = parsedUrl.pathname;
    const cookies = parseCookies(req);

    if (pathname === '/denglu.html' || pathname === '/') {
        fs.readFile('denglu.html', 'utf8', (err, data) => {
            if (err) {
                res.writeHead(404, { 'Content-Type': 'text/html; charset=UTF-8' });
                res.end('404 Not Found');
                return;
            }
            res.writeHead(200, { 'Content-Type': 'text/html; charset=UTF-8' });
            res.end(data);
        });
    } else if (pathname === '/shouye.html') {
        const session = sessions[cookies.sessionId];
        if (session) {
            fs.readFile('shouye.html', 'utf8', (err, data) => {
                if (err) {
                    res.writeHead(404, { 'Content-Type': 'text/html; charset=UTF-8' });
                    res.end('404 Not Found');
                    return;
                }
                data = data.replace('{{username}}', session.username); // 将用户名插入到首页
                res.writeHead(200, { 'Content-Type': 'text/html; charset=UTF-8' });
                res.end(data);
            });
        } else {
            res.writeHead(401, { 'Content-Type': 'text/html; charset=UTF-8' });
            res.end('请先登录');
        }
    } else if (pathname === '/zhuce.html') {
        fs.readFile('zhuce.html', 'utf8', (err, data) => {
            if (err) {
                res.writeHead(404, { 'Content-Type': 'text/html; charset=UTF-8' });
                res.end('404 Not Found');
                return;
            }
            res.writeHead(200, { 'Content-Type': 'text/html; charset=UTF-8' });
            res.end(data);
        });
    } else if (pathname === '/login' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => {
            body += chunk.toString();
        });
        req.on('end', () => {
            const parsedBody = querystring.parse(body);
            const username = parsedBody.username;
            const password = parsedBody.password;

            // 读取用户信息
            fs.readFile('user.json', 'utf8', (err, data) => {
                if (err) {
                    res.writeHead(500, { 'Content-Type': 'text/html; charset=UTF-8' });
                    res.end('服务器错误');
                    return;
                }

                const users = JSON.parse(data);
                const user = users.find(u => u.username === username && u.password === password);
                
                // 验证用户名和密码
                if (user) {
                    // 创建一个简单的会话 ID
                    const sessionId = Date.now() + Math.random().toString(36);
                    sessions[sessionId] = { username: user.username };

                    res.writeHead(302, {
                        'Set-Cookie': `sessionId=${sessionId}; HttpOnly`,
                        'Location': '/shouye.html'
                    });
                    res.end();
                } else {
                    res.writeHead(401, { 'Content-Type': 'text/html; charset=UTF-8' });
                    res.end('登录失败，用户名或密码错误');
                }
            });
        });
    } else if (pathname === '/register' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => {
            body += chunk.toString();
        });
        req.on('end', () => {
            const parsedBody = querystring.parse(body);
            const username = parsedBody.username;
            const password = parsedBody.password;

            // 读取用户信息
            fs.readFile('user.json', 'utf8', (err, data) => {
                if (err) {
                    res.writeHead(500, { 'Content-Type': 'text/html; charset=UTF-8' });
                    res.end('服务器错误');
                    return;
                }

                const users = JSON.parse(data);
                const user = users.find(u => u.username === username);
                
                // 检查用户名是否已存在
                if (user) {
                    res.writeHead(409, { 'Content-Type': 'text/html; charset=UTF-8' });
                    res.end('注册失败，用户名已存在');
                } else {
                    // 添加新用户
                    users.push({ username, password });

                    // 写入 user.json 文件
                    fs.writeFile('user.json', JSON.stringify(users, null, 2), (err) => {
                        if (err) {
                            res.writeHead(500, { 'Content-Type': 'text/html; charset=UTF-8' });
                            res.end('服务器错误');
                            return;
                        }

                        res.writeHead(302, { 'Location': '/denglu.html' });
                        res.end();
                    });
                }
            });
        });
    } else {
        res.writeHead(404, { 'Content-Type': 'text/html; charset=UTF-8' });
        res.end('404 Not Found');
    }
});

server.listen(port, hostname, () => {
    console.log(`Server running at http://${hostname}:${port}/`);
});

function parseCookies(request) {
    const list = {};
    const cookieHeader = request.headers.cookie;

    if (cookieHeader) {
        cookieHeader.split(';').forEach(cookie => {
            const parts = cookie.split('=');
            list[parts.shift().trim()] = decodeURI(parts.join('='));
        });
    }

    return list;
}
