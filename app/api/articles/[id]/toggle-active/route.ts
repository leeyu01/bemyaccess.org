import { NextRequest, NextResponse } from 'next/server';
import { supabase } from '@/lib/supabase';

// POST /api/articles/[id]/toggle-active (admin only)
export async function POST(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const authHeader = request.headers.get('authorization');
    const adminApiKey = process.env.ADMIN_API_KEY;

    if (!adminApiKey || authHeader !== `Bearer ${adminApiKey}`) {
      return NextResponse.json(
        { status: 'error', message: 'Unauthorized' },
        { status: 401 }
      );
    }

    const { data: existingArticle, error: fetchError } = await supabase
      .from('articles')
      .select('is_active')
      .eq('id', parseInt(params.id))
      .single();

    if (fetchError || !existingArticle) {
      return NextResponse.json(
        { status: 'error', message: 'Article not found' },
        { status: 404 }
      );
    }

    const newIsActive = !existingArticle.is_active;

    const { data, error } = await supabase
      .from('articles')
      .update({ is_active: newIsActive })
      .eq('id', parseInt(params.id))
      .select()
      .single();

    if (error) {
      console.error('Error toggling article active status:', error);
      return NextResponse.json(
        { status: 'error', message: error.message },
        { status: 500 }
      );
    }

    return NextResponse.json({
      status: 'success',
      data,
      message: `Article is now ${newIsActive ? 'active' : 'inactive'}`,
    });
  } catch (error) {
    console.error('Error in POST /api/articles/[id]/toggle-active:', error);
    return NextResponse.json(
      { status: 'error', message: 'Internal server error' },
      { status: 500 }
    );
  }
}
