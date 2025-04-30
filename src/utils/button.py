#===============================================================================
#modules being imported
#===============================================================================

import pygame 

#===============================================================================
#button class
#===============================================================================

class Button():
	def __init__(self,x, y, image, scale):
		WIDTH = image.get_width()
		HEIGHT = image.get_height()
		self.image = pygame.transform.scale(image, (int(WIDTH * scale), int(HEIGHT * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, screen):
		screen.blit(self.image, self.rect)
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		screen.blit(self.image, (self.rect.x, self.rect.y))

		return action