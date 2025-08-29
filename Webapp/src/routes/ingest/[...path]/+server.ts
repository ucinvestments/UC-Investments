import { error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

const POSTHOG_HOST = 'https://us.i.posthog.com';
const POSTHOG_ASSETS_HOST = 'https://us-assets.i.posthog.com';

export const GET: RequestHandler = async ({ params, url, request }) => {
  const path = params.path;
  
  // Determine target host based on path
  let targetHost = POSTHOG_HOST;
  if (path.startsWith('static/')) {
    targetHost = POSTHOG_ASSETS_HOST;
  }
  
  const targetUrl = `${targetHost}/${path}${url.search}`;
  
  try {
    const response = await fetch(targetUrl, {
      method: 'GET',
      headers: {
        'User-Agent': request.headers.get('user-agent') || '',
        'Accept': request.headers.get('accept') || '*/*',
        'Accept-Encoding': request.headers.get('accept-encoding') || '',
        'Accept-Language': request.headers.get('accept-language') || '',
      },
    });

    const body = await response.arrayBuffer();
    
    return new Response(body, {
      status: response.status,
      headers: {
        'Content-Type': response.headers.get('content-type') || 'application/octet-stream',
        'Cache-Control': response.headers.get('cache-control') || 'no-cache',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      },
    });
  } catch (err) {
    console.error('PostHog proxy error:', err);
    throw error(500, 'PostHog proxy failed');
  }
};

export const POST: RequestHandler = async ({ params, url, request }) => {
  const path = params.path;
  const targetUrl = `${POSTHOG_HOST}/${path}${url.search}`;
  
  try {
    const body = await request.arrayBuffer();
    
    const response = await fetch(targetUrl, {
      method: 'POST',
      headers: {
        'Content-Type': request.headers.get('content-type') || 'application/json',
        'User-Agent': request.headers.get('user-agent') || '',
        'Accept': request.headers.get('accept') || '*/*',
        'Accept-Encoding': request.headers.get('accept-encoding') || '',
        'Accept-Language': request.headers.get('accept-language') || '',
      },
      body,
    });

    const responseBody = await response.arrayBuffer();
    
    return new Response(responseBody, {
      status: response.status,
      headers: {
        'Content-Type': response.headers.get('content-type') || 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      },
    });
  } catch (err) {
    console.error('PostHog proxy error:', err);
    throw error(500, 'PostHog proxy failed');
  }
};

export const OPTIONS: RequestHandler = async () => {
  return new Response(null, {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  });
};