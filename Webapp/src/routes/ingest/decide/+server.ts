import { error } from '@sveltejs/kit';
import type { RequestHandler } from '@sveltejs/kit';

const POSTHOG_HOST = 'https://us.i.posthog.com';

export const POST: RequestHandler = async ({ url, request }) => {
  const targetUrl = `${POSTHOG_HOST}/decide${url.search}`;
  console.log('POST Proxy /decide:', targetUrl);
  
  try {
    const body = await request.text();
    
    const response = await fetch(targetUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': request.headers.get('user-agent') || 'UC-Investments-Proxy/1.0',
      },
      body,
    });

    const responseText = await response.text();
    console.log('PostHog decide response:', response.status, response.statusText);
    
    return new Response(responseText, {
      status: response.status,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      },
    });
  } catch (err) {
    console.error('PostHog decide proxy error:', err);
    throw error(500, 'PostHog decide proxy failed');
  }
};

export const OPTIONS: RequestHandler = async () => {
  return new Response(null, {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  });
};