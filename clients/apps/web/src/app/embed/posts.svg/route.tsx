import { Posts } from '@/components/Embed/Posts'
import { getServerURL } from '@/utils/api'
import {
  Article,
  ListResourceArticle,
  Organization,
  Storefront,
} from '@polar-sh/sdk'
import { notFound } from 'next/navigation'
const { default: satori } = require('satori')

export const runtime = 'edge'

const getStorefront = async (org: string): Promise<Storefront> => {
  const response = await fetch(`${getServerURL()}/v1/storefronts/${org}`, {
    method: 'GET',
  })
  if (response.status === 404) {
    notFound()
  }
  return await response.json()
}

const getPosts = async (
  organization: Organization,
  limit: number = 3,
  pinnedPosts: boolean = false,
): Promise<Article[]> => {
  let url = `${getServerURL()}/v1/articles/?organization_id=${organization.id}&is_pinned=${pinnedPosts}&is_published=true&visibility=public&limit=${limit}`

  const response = await fetch(url, {
    method: 'GET',
  })
  const data = (await response.json()) as ListResourceArticle
  return data.items ?? []
}

const renderPost = async (
  organization: Organization,
  posts: Article[],
  darkmode: boolean,
) => {
  const inter500 = await fetch(
    new URL('../../../assets/fonts/Inter-Regular.ttf', import.meta.url),
  ).then((res) => res.arrayBuffer())

  const inter600 = await fetch(
    new URL('../../../assets/fonts/Inter-Medium.ttf', import.meta.url),
  ).then((res) => res.arrayBuffer())

  const inter700 = await fetch(
    new URL('../../../assets/fonts/Inter-Bold.ttf', import.meta.url),
  ).then((res) => res.arrayBuffer())

  return await satori(
    <Posts organization={organization} posts={posts} darkmode={darkmode} />,
    {
      fonts: [
        {
          name: 'Inter',
          data: inter500,
          weight: 500,
          style: 'normal',
        },
        {
          name: 'Inter',
          data: inter600,
          weight: 600,
          style: 'medium',
        },
        {
          name: 'Inter',
          data: inter700,
          weight: 700,
          style: 'bold',
        },
      ],
    },
  )
}

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)

  const org = searchParams.get('org')
  const darkmode = searchParams.has('darkmode')

  if (!org) {
    return new Response('No org provided', { status: 400 })
  }

  try {
    const { organization } = await getStorefront(org)
    const [pinnedPosts, latestPosts] = await Promise.all([
      getPosts(organization, 3, true),
      getPosts(organization, 3, false),
    ])

    const posts = [...pinnedPosts, ...latestPosts].slice(0, 3)

    const svg = await renderPost(organization, posts, darkmode)

    return new Response(svg, {
      headers: {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache',
      },
      status: 200,
    })
  } catch (error) {
    console.error(error)
    // Return 1x1 pixel SVG to prevent image-not-found issues in browsers
    return new Response(
      '<svg width="1" height="1" viewBox="0 0 1 1" xmlns="http://www.w3.org/2000/svg"></svg>',
      {
        headers: {
          'Content-Type': 'image/svg+xml',
          'Cache-Control': 'no-cache',
        },
        status: 400,
      },
    )
  }
}
