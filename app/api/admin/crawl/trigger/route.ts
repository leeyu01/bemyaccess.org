import { NextRequest, NextResponse } from 'next/server';

// POST /api/admin/crawl/trigger (admin only)
export async function POST(request: NextRequest) {
  try {
    const authHeader = request.headers.get('authorization');
    const adminApiKey = process.env.ADMIN_API_KEY;

    if (!adminApiKey || authHeader !== `Bearer ${adminApiKey}`) {
      return NextResponse.json(
        { status: 'error', message: 'Unauthorized' },
        { status: 401 }
      );
    }

    // In a real implementation, this would trigger the Python crawler
    // For now, return a success message
    // TODO: Integrate with actual crawler via child_process or API call

    return NextResponse.json({
      status: 'success',
      message: 'Crawler triggered successfully (simulated)',
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    console.error('Error in POST /api/admin/crawl/trigger:', error);
    return NextResponse.json(
      { status: 'error', message: 'Internal server error' },
      { status: 500 }
    );
  }
}
