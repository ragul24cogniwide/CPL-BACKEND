import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { PrismaClient } from '@prisma/client';

dotenv.config();

const app = express();
const prisma = new PrismaClient();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// ========================
// PLAYERS API
// ========================
app.get('/api/players', async (req, res) => {
  try {
    const players = await prisma.player.findMany();
    res.json(players);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch players' });
  }
});

app.post('/api/players', async (req, res) => {
  try {
    const player = await prisma.player.create({ data: req.body });
    res.json(player);
  } catch (error) {
    res.status(500).json({ error: 'Failed to create player' });
  }
});

app.put('/api/players/:id', async (req, res) => {
  try {
    const player = await prisma.player.update({
      where: { id: req.params.id },
      data: req.body,
    });
    res.json(player);
  } catch (error) {
    res.status(500).json({ error: 'Failed to update player' });
  }
});

app.delete('/api/players/:id', async (req, res) => {
  try {
    await prisma.player.delete({ where: { id: req.params.id } });
    res.json({ message: 'Player deleted' });
  } catch (error) {
    res.status(500).json({ error: 'Failed to delete player' });
  }
});

// ========================
// TEAMS API
// ========================
app.get('/api/teams', async (req, res) => {
  try {
    const teams = await prisma.team.findMany({ include: { players: true } });
    res.json(teams);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch teams' });
  }
});

app.post('/api/teams', async (req, res) => {
  try {
    const { playerIds, ...teamData } = req.body;
    
    // Connect existing players to the team if playerIds are provided
    const data = {
      ...teamData,
      ...(playerIds && playerIds.length > 0 
          ? { players: { connect: playerIds.map((id: string) => ({ id })) } }
          : {})
    };

    const team = await prisma.team.create({ data, include: { players: true } });
    res.json(team);
  } catch (error) {
    res.status(500).json({ error: 'Failed to create team' });
  }
});

app.put('/api/teams/:id', async (req, res) => {
  try {
    const { playerIds, ...teamData } = req.body;

    const data = {
      ...teamData,
      ...(playerIds 
          ? { players: { set: playerIds.map((id: string) => ({ id })) } }
          : {})
    };

    const team = await prisma.team.update({
      where: { id: req.params.id },
      data,
      include: { players: true }
    });
    res.json(team);
  } catch (error) {
    res.status(500).json({ error: 'Failed to update team' });
  }
});

app.delete('/api/teams/:id', async (req, res) => {
  try {
    await prisma.team.delete({ where: { id: req.params.id } });
    res.json({ message: 'Team deleted' });
  } catch (error) {
    res.status(500).json({ error: 'Failed to delete team' });
  }
});


// ========================
// TOURNAMENTS API
// ========================
app.get('/api/tournaments', async (req, res) => {
  try {
    const tournaments = await prisma.tournament.findMany({ include: { teams: true, matches: true } });
    res.json(tournaments);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch tournaments' });
  }
});

app.post('/api/tournaments', async (req, res) => {
  try {
    const { teamIds, ...tournamentData } = req.body;
    const data = {
      ...tournamentData,
      ...(teamIds && teamIds.length > 0 
          ? { teams: { connect: teamIds.map((id: string) => ({ id })) } }
          : {})
    };
    const tournament = await prisma.tournament.create({ data, include: { teams: true } });
    res.json(tournament);
  } catch (error) {
    res.status(500).json({ error: 'Failed to create tournament' });
  }
});

app.put('/api/tournaments/:id', async (req, res) => {
  try {
    const { teamIds, ...tournamentData } = req.body;
    const data = {
      ...tournamentData,
      ...(teamIds 
          ? { teams: { set: teamIds.map((id: string) => ({ id })) } }
          : {})
    };
    const tournament = await prisma.tournament.update({
      where: { id: req.params.id },
      data,
      include: { teams: true }
    });
    res.json(tournament);
  } catch (error) {
    res.status(500).json({ error: 'Failed to update tournament' });
  }
});

app.delete('/api/tournaments/:id', async (req, res) => {
  try {
    await prisma.tournament.delete({ where: { id: req.params.id } });
    res.json({ message: 'Tournament deleted' });
  } catch (error) {
    res.status(500).json({ error: 'Failed to delete tournament' });
  }
});

// ========================
// MATCHES API
// ========================
app.get('/api/matches', async (req, res) => {
  try {
    const matches = await prisma.match.findMany();
    res.json(matches);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch matches' });
  }
});

app.post('/api/matches', async (req, res) => {
  try {
    const match = await prisma.match.create({ data: req.body });
    res.json(match);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Failed to create match' });
  }
});

app.put('/api/matches/:id', async (req, res) => {
  try {
    const match = await prisma.match.update({
      where: { id: req.params.id },
      data: req.body,
    });
    res.json(match);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Failed to update match' });
  }
});

app.delete('/api/matches/:id', async (req, res) => {
  try {
    await prisma.match.delete({ where: { id: req.params.id } });
    res.json({ message: 'Match deleted' });
  } catch (error) {
    res.status(500).json({ error: 'Failed to delete match' });
  }
});

// ========================
// START SERVER
// ========================
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
