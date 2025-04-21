// pages/api/contacts/[contactId]/campaigns/removeAll.ts

import type { NextApiRequest, NextApiResponse } from 'next';
import { CampaignActionResponse } from '.';
import { AuthHeaders } from '../task';

const API_BASE_URL = 'https://services.leadconnectorhq.com'; // External API base URL

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const { contactId } = req.query;

  // Validate path parameters
  if (!contactId || Array.isArray(contactId)) {
    return res.status(400).json({
      error: 'Missing or invalid path parameter: contactId is required'
    });
  }

  // Extract headers (Authorization and Version)
  const authorization = req.headers['authorization'];
  const version = req.headers['version'];

  // Validate required headers
  if (!authorization || Array.isArray(authorization)) {
    return res
      .status(401)
      .json({ error: 'Missing or invalid Authorization header' });
  }

  if (!version || Array.isArray(version)) {
    return res.status(400).json({ error: 'Missing or invalid Version header' });
  }

  // Construct headers object to match AuthHeaders type
  const headers: AuthHeaders = {
    Authorization: authorization,
    Version: version
  };

  if (req.method !== 'DELETE') {
    res.setHeader('Allow', ['DELETE']);
    return res.status(405).end(`Method ${req.method} Not Allowed`);
  }

  try {
    const apiResponse = await fetch(
      `${API_BASE_URL}/contacts/${contactId}/campaigns/removeAll`,
      {
        method: 'DELETE',
        headers: {
          Authorization: headers.Authorization,
          Version: headers.Version,
          Accept: 'application/json'
        }
      }
    );

    if (!apiResponse.ok) {
      return res.status(apiResponse.status).json({
        error: `API request failed with status ${apiResponse.status}`
      });
    }

    const data: CampaignActionResponse = await apiResponse.json();
    return res.status(200).json(data); // 200 OK
  } catch (error) {
    return res.status(500).json({ error: 'Internal Server Error' });
  }
}
