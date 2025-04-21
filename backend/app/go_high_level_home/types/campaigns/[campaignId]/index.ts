// pages/api/contacts/[contactId]/campaigns/[campaignId]/index.ts

import type { NextApiRequest, NextApiResponse } from 'next';
import { CampaignActionResponse } from '..';
import { AuthHeaders } from '../../task';

const API_BASE_URL = 'https://services.leadconnectorhq.com'; // External API base URL

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const { contactId, campaignId } = req.query;

  // Validate path parameters
  if (
    !contactId ||
    Array.isArray(contactId) ||
    !campaignId ||
    Array.isArray(campaignId)
  ) {
    return res.status(400).json({
      error:
        'Missing or invalid path parameters: contactId and campaignId are required'
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

  // Handle different HTTP methods (POST and DELETE)
  try {
    if (req.method === 'POST') {
      return await handleAddToCampaign(
        contactId as string,
        campaignId as string,
        headers,
        res
      );
    } else if (req.method === 'DELETE') {
      return await handleRemoveFromCampaign(
        contactId as string,
        campaignId as string,
        headers,
        res
      );
    } else {
      res.setHeader('Allow', ['POST', 'DELETE']);
      return res.status(405).end(`Method ${req.method} Not Allowed`);
    }
  } catch (error) {
    return res.status(500).json({ error: 'Internal Server Error' });
  }
}

// Handle POST request to add a contact to a campaign
async function handleAddToCampaign(
  contactId: string,
  campaignId: string,
  headers: AuthHeaders,
  res: NextApiResponse
) {
  const apiResponse = await fetch(
    `${API_BASE_URL}/contacts/${contactId}/campaigns/${campaignId}`,
    {
      method: 'POST',
      headers: {
        Authorization: headers.Authorization,
        Version: headers.Version,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({})
    }
  );

  if (!apiResponse.ok) {
    return res
      .status(apiResponse.status)
      .json({ error: `API request failed with status ${apiResponse.status}` });
  }

  const data: CampaignActionResponse = await apiResponse.json();
  return res.status(201).json(data); // 201 Created
}

// Handle DELETE request to remove a contact from a campaign
async function handleRemoveFromCampaign(
  contactId: string,
  campaignId: string,
  headers: AuthHeaders,
  res: NextApiResponse
) {
  const apiResponse = await fetch(
    `${API_BASE_URL}/contacts/${contactId}/campaigns/${campaignId}`,
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
    return res
      .status(apiResponse.status)
      .json({ error: `API request failed with status ${apiResponse.status}` });
  }

  const data: CampaignActionResponse = await apiResponse.json();
  return res.status(200).json(data); // 200 OK
}
